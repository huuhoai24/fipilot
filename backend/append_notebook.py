import json

notebook_path = '/home/hoai/user/resource/fipilot/backend/notebooks/04_pipeline_poc.ipynb'
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_cells = [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## 7. Interview Prepare (POST /api/v2/interview/prepare)\n",
    "Mô phỏng luồng: Nhận Profile -> Tạo Interview Config -> Gọi LLM Planner -> Trả về Interview Blueprint."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "class InterviewConfig(BaseModel):\n",
    "    role: str = Field(..., description=\"Role to interview for\")\n",
    "    level: str = Field(..., description=\"Seniority level (e.g., Junior, Mid, Senior)\")\n",
    "    duration_minutes: int = Field(30, description=\"Expected interview duration\")\n",
    "\n",
    "class InterviewRound(BaseModel):\n",
    "    round_id: int = Field(..., description=\"Order of the round\")\n",
    "    topic: str = Field(..., description=\"Main topic of this round\")\n",
    "    target_skills: List[str] = Field(..., description=\"Skills to evaluate from the candidate profile\")\n",
    "    difficulty: str = Field(..., description=\"Difficulty level (e.g., Easy, Medium, Hard)\")\n",
    "    weight_percentage: int = Field(..., description=\"Importance weight out of 100%\")\n",
    "\n",
    "class InterviewPlan(BaseModel):\n",
    "    rounds: List[InterviewRound] = Field(..., description=\"List of interview rounds\")\n",
    "    focus_areas: List[str] = Field(..., description=\"Key areas the interviewer should focus on\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def generate_interview_plan(profile: CandidateProfile, config: InterviewConfig) -> InterviewPlan:\n",
    "    llm = LLMClient()\n",
    "    \n",
    "    system_prompt = \"\"\"\n",
    "    You are an expert Technical Interview Planner.\n",
    "    Based on the candidate's profile and the interview configuration, generate a structured interview plan.\n",
    "    The plan should be divided into logical rounds, progressing from general experience to deep technical dives.\n",
    "    Only target skills that the candidate claims to have in their profile.\n",
    "    \n",
    "    Return ONLY a valid JSON object matching this schema:\n",
    "    {\n",
    "      \"rounds\": [\n",
    "        {\n",
    "          \"round_id\": 1,\n",
    "          \"topic\": \"string\",\n",
    "          \"target_skills\": [\"string\"],\n",
    "          \"difficulty\": \"string\",\n",
    "          \"weight_percentage\": 20\n",
    "        }\n",
    "      ],\n",
    "      \"focus_areas\": [\"string\"]\n",
    "    }\n",
    "    Do NOT return markdown formatting (no ```json ... ```).\n",
    "    \"\"\"\n",
    "    \n",
    "    user_prompt = f\"\"\"\n",
    "    Interview Config:\n",
    "    Role: {config.role}\n",
    "    Level: {config.level}\n",
    "    Duration: {config.duration_minutes} minutes\n",
    "\n",
    "    Candidate Profile:\n",
    "    Name: {profile.name}\n",
    "    Skills: {', '.join(profile.skills)}\n",
    "    Recent Role: {profile.recent_role}\n",
    "    Experience: {profile.years_experience} years\n",
    "    \"\"\"\n",
    "    \n",
    "    print(f\"Planning interview for {config.role} ({config.level})...\")\n",
    "    response_text = llm.generate_text(system_prompt=system_prompt, user_prompt=user_prompt, max_new_tokens=2048)\n",
    "    \n",
    "    import json_repair\n",
    "    parsed_json = json_repair.loads(response_text)\n",
    "    return InterviewPlan(**parsed_json)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Khởi tạo cấu hình phỏng vấn\n",
    "interview_config = InterviewConfig(\n",
    "    role=\"AI Engineer (Computer Vision & LLM)\",\n",
    "    level=\"Mid-level\",\n",
    "    duration_minutes=45\n",
    ")\n",
    "\n",
    "# Gọi LLM tạo kịch bản dựa trên profile đã có từ phần trước\n",
    "interview_blueprint = generate_interview_plan(profile, interview_config)\n",
    "\n",
    "print(\"\\n=== INTERVIEW BLUEPRINT ===\\n\")\n",
    "print(f\"Focus Areas: {', '.join(interview_blueprint.focus_areas)}\\n\")\n",
    "for r in interview_blueprint.rounds:\n",
    "    print(f\"Round {r.round_id}: {r.topic} ({r.difficulty} - {r.weight_percentage}%)\")\n",
    "    print(f\"  -> Target Skills: {', '.join(r.target_skills)}\\n\")\n",
    "\n",
    "print(\"[Mock Repo] Blueprint saved to cache & DB.\")\n",
    "print(\"[Mock Repo] Response: profile_version = v1\")"
   ]
  }
]

nb['cells'].extend(new_cells)

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated with Interview Prepare section.")
