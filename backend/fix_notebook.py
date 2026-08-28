import json

notebook_path = '/home/hoai/user/resource/fipilot/backend/notebooks/04_pipeline_poc.ipynb'
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the LLM Agent cell (Cell In[9])
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "def extract_profile_with_llm(text: str) -> CandidateProfile:" in source:
            new_source = """class SkillEvidence(BaseModel):
    skill: str
    evidence: str

class CandidateProfile(BaseModel):
    name: str = Field(..., description="Full name of the candidate")
    years_experience: Optional[int] = Field(None, description="Total years of experience")
    recent_role: Optional[str] = Field(None, description="Most recent job title")
    skills: List[str] = Field(default_factory=list, description="List of technical and soft skills")
    skill_evidence: List[SkillEvidence] = Field(default_factory=list, description="Evidence for extracted skills")
    is_resume: bool = Field(..., description="True if the document is a resume, False otherwise")

def extract_profile_with_llm(text: str) -> CandidateProfile:
    llm = LLMClient()
    
    system_prompt = \"\"\"
    You are an expert HR extraction system.
    Extract the candidate profile from the user's document.
    Return ONLY a valid JSON object matching this schema:
    {
      "name": "string",
      "years_experience": "integer or null",
      "recent_role": "string or null",
      "skills": ["string"],
      "skill_evidence": [{"skill": "string", "evidence": "string"}],
      "is_resume": "boolean"
    }
    If the document does not appear to be a resume/CV, set is_resume to false.
    Do NOT return markdown formatting (no ```json ... ```).
    \"\"\"
    
    user_prompt = f"Document Text:\\n{text[:5000]}"
    
    print("Calling LLM...")
    response_text = llm.generate_text(system_prompt=system_prompt, user_prompt=user_prompt, max_new_tokens=2048)
    
    try:
        import json_repair
        parsed_json = json_repair.loads(response_text)
        return CandidateProfile(**parsed_json)
    except Exception as e:
        print(f"Error parsing LLM response: {response_text}")
        raise e

if not cached_result:
    profile = extract_profile_with_llm(resume_text)
    print(f"Extracted Name: {profile.name}")
    print(f"Is Resume: {profile.is_resume}")
    print(f"Skills: {profile.skills}")
    
    # Save to cache
    MOCK_CACHE[file_hash] = profile
"""
            # Split back into lines with \n
            lines = [line + '\n' for line in new_source.split('\n')]
            # Remove trailing \n from the last element
            if lines:
                lines[-1] = lines[-1][:-1]
            cell['source'] = lines
            break

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated.")
