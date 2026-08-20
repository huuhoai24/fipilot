import asyncio
import time
import unittest
from types import SimpleNamespace

from pydantic import BaseModel
from shared.schemas.interview import InterviewPlan

from app.config.settings import Settings
from app.services.vertex_gemini_service import (
    LLMConfigurationError,
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
        models = FakeModels(responses=[SimpleNamespace(
            text='{"name":"Alice","score":9}',
            usage_metadata=SimpleNamespace(
                prompt_token_count=12,
                candidates_token_count=7,
                total_token_count=19,
            ),
        )])
        service = self.make_service(models)

        result = await service.generate_json("Return a score", MockJSONOutput)

        self.assertEqual(result.name, "Alice")
        self.assertEqual(result.score, 9)
        self.assertEqual(models.calls[0]["model"], "gemini-complex")
        config = models.calls[0]["config"]
        self.assertEqual(config.response_mime_type, "application/json")
        self.assertIs(config.response_schema, MockJSONOutput)
        self.assertEqual(service.last_usage_record["availability"], "provider_reported")
        self.assertEqual(service.last_usage_record["input_tokens"], 12)
        self.assertEqual(service.last_usage_record["output_tokens"], 7)

    async def test_generate_json_uses_sdk_parsed_result_when_text_is_unusable(self):
        models = FakeModels(responses=[SimpleNamespace(
            text="",
            parsed={"name": "Alice", "score": 9},
            usage_metadata=SimpleNamespace(
                prompt_token_count=12,
                candidates_token_count=7,
                total_token_count=19,
            ),
        )])
        service = self.make_service(
            models,
            retry_config=RetryConfig(
                max_attempts=1,
                initial_backoff_seconds=0,
                jitter_seconds=0,
            ),
        )

        result = await service.generate_json("Return a score", MockJSONOutput)

        self.assertEqual(result, MockJSONOutput(name="Alice", score=9))
        self.assertIs(models.calls[0]["config"].response_schema, MockJSONOutput)

    async def test_interview_plan_schema_accepts_valid_nested_output(self):
        models = FakeModels(responses=[SimpleNamespace(text=(
            '{"duration_minutes":5,"rounds":[{"round_id":"r1",'
            '"topic":"API design","difficulty":"medium","weight":1,'
            '"question_budget":2}]}'
        ))])
        service = self.make_service(
            models,
            retry_config=RetryConfig(max_attempts=1),
        )

        result = await service.generate_json("Build a plan", InterviewPlan)

        self.assertEqual(result.rounds[0].topic, "API design")
        self.assertEqual(result.rounds[0].difficulty, "medium")

    async def test_interview_plan_schema_rejects_invalid_contract_shapes(self):
        invalid_payloads = {
            "invalid_nested_value": (
                '{"rounds":[{"round_id":"r1","topic":"API design",'
                '"weight":2,"question_budget":1}]}'
            ),
            "missing_required_nested_field": (
                '{"rounds":[{"round_id":"r1","difficulty":"medium"}]}'
            ),
            "wrong_container_type": '{"rounds":"not-a-list"}',
            "unsupported_enum": (
                '{"rounds":[{"round_id":"r1","topic":"API design",'
                '"difficulty":"extreme"}]}'
            ),
        }
        for label, payload in invalid_payloads.items():
            with self.subTest(label=label):
                models = FakeModels(responses=[SimpleNamespace(text=payload)])
                service = self.make_service(
                    models,
                    retry_config=RetryConfig(max_attempts=1),
                )

                with self.assertRaises(LLMResponseValidationError):
                    await service.generate_json("Build a plan", InterviewPlan)

                attempt = service.attempt_records[0]
                self.assertEqual(attempt["status"], "schema_parse_failed")
                self.assertEqual(attempt["exception_category"], "schema_validation")

    async def test_generate_json_logs_safe_model_latency_metadata(self):
        models = FakeModels(responses=[SimpleNamespace(text='{"name":"Alice","score":9}')])
        service = self.make_service(models)

        with self.assertLogs("infrastructure.llm.vertex_gemini", level="INFO") as logs:
            await service.generate_json(
                "Private candidate context",
                MockJSONOutput,
                operation="test_scoring",
            )

        record = next(item for item in logs.records if item.event == "llm.generate_json")
        self.assertEqual(record.model, "gemini-complex")
        self.assertEqual(record.task_type, "complex")
        self.assertGreater(record.prompt_chars, len("Private candidate context"))
        self.assertEqual(record.attempt, 1)
        self.assertEqual(record.operation, "test_scoring")
        self.assertEqual(record.output_schema, "MockJSONOutput")
        self.assertGreaterEqual(record.duration_ms, 0)
        self.assertFalse(hasattr(record, "prompt"))

        by_event = {item.event: item for item in logs.records}
        self.assertTrue(
            {
                "llm.request_preparation",
                "llm.model_request",
                "llm.response_parsing",
                "llm.operation_total",
                "llm.generate_json",
            }.issubset(by_event)
        )
        self.assertEqual(by_event["llm.model_request"].attempt, 1)
        self.assertEqual(
            by_event["llm.response_parsing"].response_chars,
            len('{"name":"Alice","score":9}'),
        )
        self.assertFalse(hasattr(by_event["llm.response_parsing"], "response"))

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
        models = FakeModels(responses=[
            SimpleNamespace(
                text="bad",
                usage_metadata=SimpleNamespace(
                    prompt_token_count=8,
                    candidates_token_count=2,
                    total_token_count=10,
                ),
            ),
            SimpleNamespace(text='{"name":"Missing score"}'),
        ])
        service = self.make_service(models, retry_config=RetryConfig(max_attempts=2, initial_backoff_seconds=0, jitter_seconds=0))

        with self.assertRaises(LLMResponseValidationError):
            await service.generate_json("Return a score", MockJSONOutput)

        self.assertEqual(len(service.attempt_records), 2)
        first, second = service.attempt_records
        self.assertEqual(first["status"], "schema_parse_failed")
        self.assertTrue(first["provider_request_sent"])
        self.assertTrue(first["provider_response_received"])
        self.assertEqual(first["schema_parse"], "failed")
        self.assertEqual(first["usage"]["availability"], "provider_reported")
        self.assertEqual(first["usage"]["total_tokens"], 10)
        self.assertEqual(first["exception_category"], "invalid_json")
        self.assertEqual(second["exception_category"], "schema_validation")
        self.assertEqual(second["validation_errors"][0]["loc"], ["score"])
        self.assertNotIn("response", first)
        self.assertNotIn("prompt", first)

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

    async def test_generate_json_timeout_records_failed_provider_attempt(self):
        models = FakeModels(sleep_seconds=0.05)
        service = self.make_service(
            models,
            retry_config=RetryConfig(max_attempts=1),
            default_timeout_seconds=0.001,
        )

        with self.assertRaises(LLMTimeoutError):
            await service.generate_json("Slow JSON", MockJSONOutput)

        self.assertEqual(len(service.attempt_records), 1)
        attempt = service.attempt_records[0]
        self.assertEqual(attempt["status"], "failed")
        self.assertTrue(attempt["provider_request_sent"])
        self.assertFalse(attempt["provider_response_received"])
        self.assertEqual(attempt["usage"]["availability"], "unavailable")
        self.assertEqual(attempt["exception_category"], "timeout")

    async def test_generate_json_exposes_configuration_failure_before_request(self):
        settings = Settings(
            APP_ENV="test",
            GOOGLE_CLOUD_PROJECT=None,
            GEMINI_SIMPLE_MODEL="gemini-simple",
            GEMINI_COMPLEX_MODEL="gemini-complex",
        )
        service = VertexGeminiService(
            settings=settings,
            retry_config=RetryConfig(max_attempts=1),
        )

        with self.assertRaisesRegex(
            LLMConfigurationError,
            "GOOGLE_CLOUD_PROJECT is required",
        ):
            await service.generate_json("Build a plan", InterviewPlan)

        attempt = service.attempt_records[0]
        self.assertFalse(attempt["provider_request_sent"])
        self.assertFalse(attempt["provider_response_received"])
        self.assertEqual(attempt["exception_type"], "LLMConfigurationError")
        self.assertEqual(attempt["exception_category"], "configuration_error")
        self.assertNotIn(
            "provider_request_sent",
            [event["state"] for event in attempt["events"]],
        )

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
