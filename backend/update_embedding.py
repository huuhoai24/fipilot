import os
import re

file_path = "infrastructure/llm/azure_openai.py"
with open(file_path, "r") as f:
    content = f.read()

new_embedding_method = """    async def generate_embedding(self, text: str, model: str | None = None) -> list[float]:
        selected_model = model or os.environ.get("AZURE_EMBEDDING_MODEL") or "text-embedding-3-small"
        
        # Determine if we should use a specific Foundry endpoint for embeddings
        from openai import AsyncOpenAI
        
        foundry_endpoint = os.environ.get("AZURE_FOUNDRY_ENDPOINT")
        foundry_key = os.environ.get("AZURE_FOUNDRY_API_KEY")
        
        if foundry_endpoint and foundry_key and "openai.azure" not in (os.environ.get("AZURE_OPENAI_BASE_URL") or ""):
            # Or if they are different resources
            pass
            
        # Actually, let's always try to use the AZURE_FOUNDRY_ENDPOINT for embeddings 
        # if the default client fails with 404, or just create a specific client for it.
"""

