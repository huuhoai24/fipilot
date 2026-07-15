import os
import pypdf
import docx
from openai import AsyncOpenAI
import json

class CVExtractor:
    def __init__(self):
        # Default to Ollama local instance if not provided
        base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        api_key = os.environ.get("OLLAMA_API_KEY", "ollama")
        # Sử dụng model gemma4:e2b theo yêu cầu
        self.model = os.environ.get("OLLAMA_CV_MODEL", "gemma4:e2b")
        self.client = AsyncOpenAI(base_url=base_url, api_key=api_key)

    def extract_text(self, file_path: str, filename: str) -> str:
        text = ""
        ext = filename.split('.')[-1].lower()
        try:
            if ext == "pdf":
                with open(file_path, "rb") as f:
                    reader = pypdf.PdfReader(f)
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            elif ext in ["docx", "doc"]:
                doc = docx.Document(file_path)
                for para in doc.paragraphs:
                    text += para.text + "\n"
        except Exception as e:
            print(f"Error parsing CV: {e}")
        return text.strip()

    async def parse_cv(self, text: str) -> dict:
        prompt = f"""
You are an expert technical recruiter. Extract the following information from the provided CV.
Return ONLY a valid JSON object with the following exact keys:
- "candidate_name": string (the candidate's full name)
- "years_experience": float (total years of professional experience, estimate if needed)
- "skills": list of strings (key technical skills like Python, React, SQL, etc.)
- "education": string (highest degree and university)
- "recent_role": string (the most recent job title and company)
- "inferred_level": integer (1 for Junior/Entry, 2 for Mid-level, 3 for Senior, 4 for Lead/Principal based on experience)
- "role_fit": string (one of: 'Data Engineer', 'AI Engineer', 'Backend Developer', 'Frontend Developer', 'Web Developer', 'DevOps Engineer', 'Tester', 'Business Analyst', 'Software Engineer', 'Data Scientist')

CV Text:
{text[:4000]}
"""
        print(f"Calling Ollama model {self.model} for CV extraction...")
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            result = response.choices[0].message.content
            # Clean up potential markdown formatting around JSON
            result = result.strip()
            if result.startswith("```json"):
                result = result[7:]
            if result.endswith("```"):
                result = result[:-3]
                
            return json.loads(result)
        except Exception as e:
            print(f"LLM Extraction Error: {e}")
            # Fallback data if extraction fails
            return {
                "candidate_name": "Ứng viên (Parse Error)",
                "years_experience": 1.0,
                "skills": ["Not Found"],
                "education": "Not Found",
                "recent_role": "Not Found",
                "inferred_level": 1,
                "role_fit": "Software Engineer",
                "confidence": 0.0
            }

cv_extractor = CVExtractor()
