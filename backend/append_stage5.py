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
    "## 10. Report Generation (POST /api/v2/interview/{id}/report)\n",
    "Mô phỏng Giai đoạn 5: Tổng hợp điểm số (Math) -> Gọi AI sinh Coaching Feedback -> Xuất Báo cáo chuẩn Chakra."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def generate_coaching_feedback(evaluations: List[EvidenceEvaluation]) -> str:\n",
    "    llm = LLMClient()\n",
    "    \n",
    "    # Lọc ra các lỗ hổng\n",
    "    gaps = [ev for ev in evaluations if ev.status in [ExpectationStatus.MISSING, ExpectationStatus.PARTIAL]]\n",
    "    if not gaps:\n",
    "        return \"Tuyệt vời! Bạn đã trả lời xuất sắc tất cả các tiêu chí.\"\n",
    "        \n",
    "    gap_descriptions = \"\\n\".join([f\"- {ev.key_point} (Lý do: {ev.reasoning})\" for ev in gaps])\n",
    "    \n",
    "    system_prompt = \"\"\"\n",
    "    You are an expert AI Interview Coach.\n",
    "    Based on the candidate's missing or partial gaps during the interview, write a short, constructive, and highly actionable coaching feedback block in VIETNAMESE.\n",
    "    Tell the candidate exactly what they missed and how they can improve their answers in actual job interviews.\n",
    "    Return ONLY the raw string of the feedback (no markdown formatting, no JSON).\n",
    "    \"\"\"\n",
    "    \n",
    "    user_prompt = f\"Candidate Gaps:\\n{gap_descriptions}\"\n",
    "    \n",
    "    return llm.generate_text(system_prompt=system_prompt, user_prompt=user_prompt, max_new_tokens=500).strip()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Giả lập việc gom toàn bộ đánh giá của phiên phỏng vấn (Trong thực tế sẽ lấy từ Database)\n",
    "# Ở đây ta dùng lại biến `evaluation` từ Bước 9\n",
    "\n",
    "def generate_final_report(all_evaluations: List[EvidenceEvaluation]):\n",
    "    print(\"===============================================\")\n",
    "    print(\"       HACKERRANK CHAKRA-STYLE SCORECARD       \")\n",
    "    print(\"===============================================\\n\")\n",
    "    \n",
    "    # 1. Tính toán điểm số\n",
    "    score_map = {\"MET\": 3, \"PARTIAL\": 2, \"MISSING\": 1}\n",
    "    total_possible = len(all_evaluations) * 3\n",
    "    total_earned = sum([score_map[ev.status] for ev in all_evaluations])\n",
    "    \n",
    "    # Chuẩn hóa về thang 5.0\n",
    "    normalized_score = (total_earned / total_possible) * 5.0 if total_possible > 0 else 0\n",
    "    \n",
    "    print(f\"⭐ OVERALL SCORE: {normalized_score:.1f} / 5.0\\n\")\n",
    "    \n",
    "    # 2. Báo cáo Bằng chứng (Evidence-Anchored Breakdown)\n",
    "    print(\"🔍 EVIDENCE-ANCHORED BREAKDOWN:\")\n",
    "    for idx, ev in enumerate(all_evaluations, 1):\n",
    "        status_color = \"✅\" if ev.status == \"MET\" else (\"⚠️\" if ev.status == \"PARTIAL\" else \"❌\")\n",
    "        print(f\"  {idx}. {ev.key_point} {status_color}\")\n",
    "        if ev.evidence:\n",
    "            print(f\"     > Bằng chứng (Trích xuất từ Transcript): \\\"{ev.evidence}\\\"\")\n",
    "        else:\n",
    "            print(f\"     > Bằng chứng: [Không tìm thấy bằng chứng trong Transcript]\")\n",
    "        print(f\"     > Đánh giá: {ev.reasoning}\\n\")\n",
    "        \n",
    "    # 3. Lời khuyên (Coaching Feedback)\n",
    "    print(\"💡 ACTIONABLE COACHING FEEDBACK:\")\n",
    "    print(\"Đang phân tích lỗ hổng để sinh lời khuyên...\")\n",
    "    coaching_advice = generate_coaching_feedback(all_evaluations)\n",
    "    print(f\"> {coaching_advice}\")\n",
    "\n",
    "# Chạy hàm sinh Report với kết quả từ Câu hỏi 1 (Giả sử ta chỉ hỏi 1 câu)\n",
    "# Vì ở Bước 9 ta lưu kết quả vào biến local, ta cần gọi lại hàm evaluate_answer để lấy data, \n",
    "# hoặc bạn có thể pass trực tiếp data nếu đang lưu global. Ở đây ta giả sử đã có data:\n",
    "# evaluation = evaluate_answer(first_question_result.question_text, first_question_result.expected_key_points, mock_candidate_answer)\n",
    "print(\"Bắt đầu xuất Report...\\n\")\n",
    "# generate_final_report(evaluation.evaluations) # Bỏ comment dòng này sau khi lưu biến evaluation global ở bước 9\n"
   ]
  }
]

# Modify Cell 9 slightly to save evaluation as a global variable so Cell 10 can use it
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if "def process_answer(" in source:
            new_source = source.replace(
                "    evaluation = evaluate_answer(question_text, expected_points, candidate_answer)",
                "    global global_evaluation_mock\n    global_evaluation_mock = evaluate_answer(question_text, expected_points, candidate_answer)\n    evaluation = global_evaluation_mock"
            )
            lines = [line + '\n' for line in new_source.split('\n')]
            if lines:
                lines[-1] = lines[-1][:-1]
            cell['source'] = lines
        if "generate_final_report(evaluation.evaluations)" in source: # Just in case
            pass

# Ensure we use global_evaluation_mock in the last cell
new_cells[-1]['source'][-1] = "if 'global_evaluation_mock' in globals():\n    generate_final_report(global_evaluation_mock.evaluations)\nelse:\n    print('Vui lòng chạy lại Cell 9 để lưu dữ liệu trước khi xuất Report!')"

nb['cells'].extend(new_cells)

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated with Stage 5 (Report Generation).")
