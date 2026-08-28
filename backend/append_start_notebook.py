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
    "## 8. Interview Start (POST /api/v2/interview/start)\n",
    "Mô phỏng luồng: Khởi tạo Session -> Lấy Round 1 -> Gọi QuestionGeneratorAgent tạo câu hỏi kỹ thuật đầu tiên (bỏ qua Opening Message)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "class QuestionGenerationResult(BaseModel):\n",
    "    question_text: str = Field(..., description=\"The actual question to ask the candidate\")\n",
    "    expected_key_points: List[str] = Field(..., description=\"Key points expected in a good answer\")\n",
    "\n",
    "def generate_first_question(profile: CandidateProfile, first_round: InterviewRound) -> QuestionGenerationResult:\n",
    "    llm = LLMClient()\n",
    "    \n",
    "    system_prompt = \"\"\"\n",
    "    You are a technical interviewer for an AI Engineering role.\n",
    "    Your task is to generate the VERY FIRST technical question for the candidate based on their profile and the current interview round.\n",
    "    \n",
    "    IMPORTANT RULES:\n",
    "    1. DO NOT include any greetings, pleasantries, or opening messages (e.g., no \"Hello\", no \"Welcome\").\n",
    "    2. Get straight to the technical question.\n",
    "    3. Ask exactly ONE clear, concise question related to the Target Skills.\n",
    "    4. Base the context of the question on the candidate's actual experience if possible.\n",
    "    \n",
    "    Return ONLY a valid JSON object matching this schema:\n",
    "    {\n",
    "      \"question_text\": \"string\",\n",
    "      \"expected_key_points\": [\"string\"]\n",
    "    }\n",
    "    Do NOT return markdown formatting (no ```json ... ```).\n",
    "    \"\"\"\n",
    "    \n",
    "    user_prompt = f\"\"\"\n",
    "    Candidate Name: {profile.name}\n",
    "    Candidate Experience/Skills: {', '.join(profile.skills)}\n",
    "    \n",
    "    Current Round Topic: {first_round.topic}\n",
    "    Target Skills for this Round: {', '.join(first_round.target_skills)}\n",
    "    Difficulty: {first_round.difficulty}\n",
    "    \"\"\"\n",
    "    \n",
    "    print(\"Calling QuestionGeneratorAgent...\")\n",
    "    response_text = llm.generate_text(system_prompt=system_prompt, user_prompt=user_prompt, max_new_tokens=1024)\n",
    "    \n",
    "    import json_repair\n",
    "    parsed_json = json_repair.loads(response_text)\n",
    "    return QuestionGenerationResult(**parsed_json)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import uuid\n",
    "\n",
    "# 1. Lấy Round đầu tiên từ Blueprint\n",
    "first_round = interview_blueprint.rounds[0]\n",
    "print(f\"[Orchestrator] Starting Round 1: {first_round.topic}\")\n",
    "\n",
    "# 2. QuestionGeneratorAgent tạo câu hỏi đầu tiên (Không có Opening Message)\n",
    "first_question_result = generate_first_question(profile, first_round)\n",
    "\n",
    "# 3. Tạo Session và State\n",
    "session_id = str(uuid.uuid4())\n",
    "session_state = {\n",
    "    \"session_id\": session_id,\n",
    "    \"status\": \"IN_PROGRESS\",\n",
    "    \"current_round_id\": first_round.round_id,\n",
    "    \"turn_count\": 1\n",
    "}\n",
    "\n",
    "print(\"\\n=== API RESPONSE (Interview Start) ===\")\n",
    "print(f\"Session ID: {session_id}\")\n",
    "print(\"\\n[AI Interviewer Asks]:\")\n",
    "print(f\"> {first_question_result.question_text}\")\n",
    "print(\"\\n[Expected Key Points (Hidden from Candidate)]:\")\n",
    "for pt in first_question_result.expected_key_points:\n",
    "    print(f\"- {pt}\")"
   ]
  }
]

nb['cells'].extend(new_cells)

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated with Interview Start section.")
