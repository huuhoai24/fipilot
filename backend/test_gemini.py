import asyncio

from app.services.vertex_gemini_service import VertexGeminiService


async def main():

    llm = VertexGeminiService()

    response = await llm.generate_text(
        "Explain YOLO object detection in 3 sentences"
    )

    print(response)


if __name__ == "__main__":
    asyncio.run(main())