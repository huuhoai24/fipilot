import asyncio
import time
import unittest
from types import SimpleNamespace

from pydantic import BaseModel

from app.config.settings import Settings
from app.services.vertex_gemini_service import (
    LLMResponseValidationError,
    LLMTimeoutError,
    RetryConfig,
    VertexGeminiService,
)


class MockJSONOutput(BaseModel):
    name: str
    score: int


class FakeModels:
    def __init__(self, responses=None, errors=None, sleep_seconds: float = 0.0):
        self.responses = list(responses or [])
        self.errors = list(errors or [])
        self.sleep_seconds = sleep_seconds
        self.calls = []

    def generate_content(self, **kwargs):
        self.calls.append(kwargs)
        if self.sleep_seconds:
            time.sleep(self.sleep_seconds)
        if self.errors:
            error = self.errors.pop(0)
            if error is not None:
                raise error
        if self.responses:
            return self.responses.pop(0)
        return SimpleNamespace(text="fallback response")


class FakeClient:
    def __init__(self, models, async_models=None):
        self.models = models
        self.aio = SimpleNamespace(models=async_models)


class FakeAsyncModels:
    def __init__(self, responses=None, errors=None):
        self.responses = list(responses or [])
        self.errors = list(errors or [])
        self.calls = []

    async def generate_content_stream(self, **kwargs):
        self.calls.append(kwargs)
        if self.errors:
            error = self.errors.pop(0)
            if error is not None:
                raise error

        async def iterate():
            for response in self.responses:
                yield response

        return iterate()


class VertexGeminiServiceTests(unittest.IsolatedAsyncioTestCase):
    def make_service(self, models, *, async_models=None, **kwargs):
        settings = Settings(
            APP_ENV="test",
            GOOGLE_CLOUD_PROJECT="unit-test-project",
            GEMINI_SIMPLE_MODEL="gemini-simple",
            GEMINI_COMPLEX_MODEL="gemini-complex",
        )
        retry_config = kwargs.pop("retry_config", RetryConfig(max_attempts=2, initial_backoff_seconds=0, jitter_seconds=0))
        return VertexGeminiService(
            settings=settings,
            client=FakeClient(models, async_models),
            retry_config=retry_config,
            default_timeout_seconds=kwargs.pop("default_timeout_seconds", 5),
            **kwargs,
        )

    async def test_route_model_uses_simple_and_complex_settings(self):
        service = self.make_service(FakeModels())

        self.assertEqual(service.route_model("simple"), "gemini-simple")
        self.assertEqual(service.route_model("complex"), "gemini-complex")
        self.assertEqual(service.route_model("simple", model="explicit-model"), "explicit-model")

    async def test_generate_text_calls_vertex_client(self):
        models = FakeModels(responses=[SimpleNamespace(text="Hello candidate")])
        service = self.make_service(models)

        result = await service.generate_text("Say hello", task_type="simple")

        self.assertEqual(result, "Hello candidate")
        self.assertEqual(models.calls[0]["model"], "gemini-simple")
        self.assertEqual(models.calls[0]["contents"], "Say hello")

    async def test_generate_json_validates_with_pydantic_schema(self):
        models = FakeModels(responses=[SimpleNamespace(text='{"name":"Alice","score":9}')])
        service = self.make_service(models)

        result = await service.generate_json("Return a score", MockJSONOutput)

        self.assertEqual(result.name, "Alice")
        self.assertEqual(result.score, 9)
        self.assertEqual(models.calls[0]["model"], "gemini-complex")
        config = models.calls[0]["config"]
        self.assertEqual(config.response_mime_type, "application/json")
        self.assertEqual(config.response_json_schema["title"], "MockJSONOutput")

    async def test_generate_json_can_disable_thinking(self):
        models = FakeModels(responses=[SimpleNamespace(text='{"name":"Alice","score":9}')])
        service = self.make_service(models)

        await service.generate_json(
            "Return a score",
            MockJSONOutput,
            task_type="simple",
            thinking_budget=0,
        )

        config = models.calls[0]["config"]
        self.assertEqual(models.calls[0]["model"], "gemini-simple")
        self.assertEqual(config.thinking_config.thinking_budget, 0)

    async def test_generate_json_extracts_json_from_markdown(self):
        models = FakeModels(responses=[SimpleNamespace(text='```json\n{"name":"Bob","score":7}\n```')])
        service = self.make_service(models)

        result = await service.generate_json("Return a score", MockJSONOutput)

        self.assertEqual(result.name, "Bob")
        self.assertEqual(result.score, 7)

    async def test_generate_json_retries_invalid_json(self):
        models = FakeModels(
            responses=[
                SimpleNamespace(text="not json"),
                SimpleNamespace(text='{"name":"Retry Works","score":8}'),
            ]
        )
        service = self.make_service(models, retry_config=RetryConfig(max_attempts=2, initial_backoff_seconds=0, jitter_seconds=0))

        result = await service.generate_json("Return a score", MockJSONOutput)

        self.assertEqual(result.name, "Retry Works")
        self.assertEqual(len(models.calls), 2)

    async def test_generate_json_raises_after_validation_retries(self):
        models = FakeModels(responses=[SimpleNamespace(text="bad"), SimpleNamespace(text='{"name":"Missing score"}')])
        service = self.make_service(models, retry_config=RetryConfig(max_attempts=2, initial_backoff_seconds=0, jitter_seconds=0))

        with self.assertRaises(LLMResponseValidationError):
            await service.generate_json("Return a score", MockJSONOutput)

    async def test_generate_text_retries_retryable_error(self):
        models = FakeModels(
            responses=[SimpleNamespace(text="Recovered")],
            errors=[RuntimeError("temporarily unavailable"), None],
        )
        service = self.make_service(models, retry_config=RetryConfig(max_attempts=2, initial_backoff_seconds=0, jitter_seconds=0))

        result = await service.generate_text("Say hello")

        self.assertEqual(result, "Recovered")
        self.assertEqual(len(models.calls), 2)

    async def test_generate_text_timeout(self):
        models = FakeModels(sleep_seconds=0.05)
        service = self.make_service(models, retry_config=RetryConfig(max_attempts=1), default_timeout_seconds=0.001)

        with self.assertRaises(LLMTimeoutError):
            await service.generate_text("Slow prompt")

    async def test_stream_text_yields_ordered_vertex_deltas(self):
        async_models = FakeAsyncModels(
            responses=[
                SimpleNamespace(text="Can you explain"),
                SimpleNamespace(text=" YOLO architecture?"),
            ]
        )
        service = self.make_service(
            FakeModels(),
            async_models=async_models,
        )

        deltas = [
            delta
            async for delta in service.stream_text(
                "Generate one question",
                task_type="complex",
                output_schema=MockJSONOutput,
            )
        ]

        self.assertEqual(
            deltas,
            ["Can you explain", " YOLO architecture?"],
        )
        self.assertEqual(
            async_models.calls[0]["model"],
            "gemini-complex",
        )
        config = async_models.calls[0]["config"]
        self.assertEqual(config.response_mime_type, "application/json")
        self.assertEqual(config.response_json_schema["title"], "MockJSONOutput")


if __name__ == "__main__":
    unittest.main()
