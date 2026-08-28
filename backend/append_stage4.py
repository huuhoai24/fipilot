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
    "## 9. Submit Answer (Evidence-Based Evaluation & Adaptive Probing)\n",
    "Mô phỏng Giai đoạn 4: Nhận câu trả lời -> Dùng Evaluator chấm theo Barem (MET/MISSING) -> Decision Controller quyết định Follow-up."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "from enum import Enum\n",
    "\n",
    "class ExpectationStatus(str, Enum):\n",
    "    MET = \"MET\"\n",
    "    PARTIAL = \"PARTIAL\"\n",
    "    MISSING = \"MISSING\"\n",
    "\n",
    "class EvidenceEvaluation(BaseModel):\n",
    "    key_point: str = Field(..., description=\"The expected key point being evaluated\")\n",
    "    status: ExpectationStatus = Field(..., description=\"Status of the evaluation (MET, PARTIAL, MISSING)\")\n",
    "    evidence: Optional[str] = Field(None, description=\"Direct quote or proof from the answer, if any\")\n",
    "    reasoning: str = Field(..., description=\"Brief explanation of why this status was given\")\n",
    "\n",
    "class AnswerEvaluationResult(BaseModel):\n",
    "    evaluations: List[EvidenceEvaluation] = Field(..., description=\"Evaluation for each expected key point\")\n",
    "    overall_assessment: str = Field(..., description=\"Short summary of the candidate's performance on this question\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def evaluate_answer(question: str, expected_points: List[str], candidate_answer: str) -> AnswerEvaluationResult:\n",
    "    llm = LLMClient()\n",
    "    system_prompt = \"\"\"\n",
    "    You are a strict, evidence-based technical interviewer.\n",
    "    Evaluate the candidate's answer against the Expected Key Points.\n",
    "    For EACH key point, you must assign a status:\n",
    "    - MET: The candidate clearly and accurately addressed this with specificity.\n",
    "    - PARTIAL: The candidate touched on this, but lacked depth, specificity, or examples.\n",
    "    - MISSING: The candidate completely failed to address this or was incorrect.\n",
    "    \n",
    "    You MUST extract a direct quote (`evidence`) from the candidate's answer if the status is MET or PARTIAL.\n",
    "    Do NOT guess or assume. If it's not explicitly in the answer, it's MISSING.\n",
    "    \n",
    "    Return ONLY a valid JSON object matching the requested schema.\n",
    "    \"\"\"\n",
    "    \n",
    "    user_prompt = f\"\"\"\n",
    "    Question Asked: {question}\n",
    "    Expected Key Points: {expected_points}\n",
    "    Candidate's Answer: {candidate_answer}\n",
    "    \"\"\"\n",
    "    \n",
    "    response_text = llm.generate_text(system_prompt=system_prompt, user_prompt=user_prompt, max_new_tokens=1500)\n",
    "    \n",
    "    import json_repair\n",
    "    parsed_json = json_repair.loads(response_text)\n",
    "    return AnswerEvaluationResult(**parsed_json)\n",
    "\n",
    "def generate_followup_question(original_question: str, candidate_answer: str, missing_point: str) -> str:\n",
    "    llm = LLMClient()\n",
    "    system_prompt = \"\"\"\n",
    "    You are an adaptive AI interviewer.\n",
    "    The candidate missed or was superficial about a specific expectation in their previous answer.\n",
    "    Generate a SINGLE, sharp follow-up question to probe the candidate specifically on this missing expectation.\n",
    "    DO NOT repeat the original question. Just ask the follow-up directly.\n",
    "    The question MUST be written in VIETNAMESE.\n",
    "    Return ONLY the string of the question (no JSON, no markdown).\n",
    "    \"\"\"\n",
    "    user_prompt = f\"\"\"\n",
    "    Original Question: {original_question}\n",
    "    Candidate Answer: {candidate_answer}\n",
    "    Missing/Partial Expectation to Probe: {missing_point}\n",
    "    \"\"\"\n",
    "    return llm.generate_text(system_prompt=system_prompt, user_prompt=user_prompt, max_new_tokens=256).strip()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def process_answer(question_text: str, expected_points: List[str], candidate_answer: str):\n",
    "    print(\"\\n===============================================\")\n",
    "    print(\"[Ứng viên trả lời]:\")\n",
    "    print(f\"> {candidate_answer}\\n\")\n",
    "    \n",
    "    print(\"--- 1. EVALUATOR AGENT CHẤM ĐIỂM (EVIDENCE-BASED) ---\")\n",
    "    evaluation = evaluate_answer(question_text, expected_points, candidate_answer)\n",
    "    \n",
    "    missing_gaps = []\n",
    "    for ev in evaluation.evaluations:\n",
    "        status_color = \"✅\" if ev.status == \"MET\" else (\"⚠️\" if ev.status == \"PARTIAL\" else \"❌\")\n",
    "        print(f\"{status_color} [{ev.status}] Tiêu chí: {ev.key_point}\")\n",
    "        if ev.evidence:\n",
    "            print(f\"    Lý do: {ev.reasoning} (Bằng chứng: '{ev.evidence}')\")\n",
    "        else:\n",
    "            print(f\"    Lý do: {ev.reasoning}\")\n",
    "        \n",
    "        # Phân loại gap để tính toán Belief State\n",
    "        if ev.status in [\"MISSING\", \"PARTIAL\"]:\n",
    "            missing_gaps.append(ev.key_point)\n",
    "            \n",
    "    print(f\"\\nĐánh giá chung: {evaluation.overall_assessment}\")\n",
    "    \n",
    "    print(\"\\n--- 2. DECISION CONTROLLER (FOLLOW-UP) ---\")\n",
    "    if missing_gaps:\n",
    "        # Thuật toán Information Gain: Chọn gap đầu tiên (hoặc lớn nhất) để đào sâu\n",
    "        target_gap = missing_gaps[0] \n",
    "        print(f\"[Policy] Phát hiện lỗ hổng. Trigger cờ FOLLOW_UP cho tiêu chí: '{target_gap}'\")\n",
    "        \n",
    "        follow_up_q = generate_followup_question(question_text, candidate_answer, target_gap)\n",
    "        print(\"\\n[AI Interviewer Hỏi Xoáy]:\")\n",
    "        print(f\"> {follow_up_q}\")\n",
    "    else:\n",
    "        print(\"[Policy] Ứng viên đạt đủ kỳ vọng. Trigger cờ NEXT_QUESTION (Chuyển câu tiếp theo).\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Chạy giả lập (Mock Simulation)\n",
    "# Tình huống: Ứng viên trả lời rất hời hợt, thiếu chiều sâu so với câu hỏi kỹ thuật ở Bước 8\n",
    "\n",
    "mock_candidate_answer = \"Tôi nghĩ ngôn ngữ này khá dễ dùng và có nhiều thư viện hỗ trợ. Trong các dự án của tôi, tôi thường dùng nó để xử lý dữ liệu và viết vài script tự động hoá cơ bản.\"\n",
    "\n",
    "process_answer(\n",
    "    first_question_result.question_text, \n",
    "    first_question_result.expected_key_points, \n",
    "    mock_candidate_answer\n",
    ")"
   ]
  }
]

nb['cells'].extend(new_cells)

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated with Stage 4 (Evidence-Based Evaluation).")
