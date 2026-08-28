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
    "## 6.5. RAG Retrieval Mock (Dùng Focus Areas để Vector Search)\n",
    "Thử nghiệm ý tưởng: Dùng đoạn `Focus Areas` trong CV để search ra Top các bài học (Knowledge) phù hợp nhất bằng kỹ thuật Semantic Search (Ở đây dùng TF-IDF Cosine Similarity để mô phỏng Vector Search mà không cần cài thêm Database nặng)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.feature_extraction.text import TfidfVectorizer\n",
    "from sklearn.metrics.pairwise import cosine_similarity\n",
    "import os\n",
    "import glob\n",
    "\n",
    "def mock_vector_search(query: str, top_k: int = 3):\n",
    "    # 1. Đọc danh sách các file Knowledge (Đóng vai trò là Vector Database)\n",
    "    knowledge_dir = str(Path(os.getcwd()).parent / \"Knowledge\" / \"Domains\" / \"AI_Enginner\")\n",
    "    \n",
    "    # Lấy thử một vài file trong thư mục LLM và Computer Vision để làm mẫu\n",
    "    search_patterns = [\n",
    "        f\"{knowledge_dir}/**/*.md\"\n",
    "    ]\n",
    "    \n",
    "    doc_paths = []\n",
    "    for pattern in search_patterns:\n",
    "        doc_paths.extend(glob.glob(pattern, recursive=True))\n",
    "        \n",
    "    documents = []\n",
    "    doc_names = []\n",
    "    for path in doc_paths:\n",
    "        with open(path, 'r', encoding='utf-8') as f:\n",
    "            documents.append(f.read())\n",
    "            # Lấy tên thư mục cha + tên file để dễ nhìn\n",
    "            doc_names.append(\"/\\\\\".join(path.split(os.sep)[-2:]))\n",
    "            \n",
    "    if not documents:\n",
    "        return \"Không tìm thấy file Knowledge nào để search.\"\n",
    "\n",
    "    # 2. Embedding (Mô phỏng bằng TF-IDF)\n",
    "    vectorizer = TfidfVectorizer(stop_words='english')\n",
    "    # Đưa cả query và documents vào không gian Vector\n",
    "    all_texts = [query] + documents\n",
    "    tfidf_matrix = vectorizer.fit_transform(all_texts)\n",
    "    \n",
    "    # 3. Tính độ tương đồng (Cosine Similarity) giữa Query (index 0) và Documents (index 1..N)\n",
    "    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()\n",
    "    \n",
    "    # Lấy Top K kết quả cao nhất\n",
    "    top_indices = cosine_similarities.argsort()[-top_k:][::-1]\n",
    "    \n",
    "    print(\"===============================================\")\n",
    "    print(\"[INPUT QUERY - Focus Areas từ CV]:\")\n",
    "    print(f\"> {query}\\n\")\n",
    "    print(\"[KẾT QUẢ VECTOR SEARCH (Top Documents)]: \")\n",
    "    \n",
    "    for i, idx in enumerate(top_indices):\n",
    "        score = cosine_similarities[idx]\n",
    "        print(f\"{i+1}. Document: {doc_names[idx]}\")\n",
    "        print(f\"   - Mức độ phù hợp (Similarity Score): {score:.4f}\\n\")\n",
    "        \n",
    "    return [doc_names[idx] for idx in top_indices]\n",
    "\n",
    "# Chạy giả lập với ý tưởng của bạn\n",
    "focus_areas_query = \"Computer Vision model development and optimization, Deep Learning frameworks usage and deployment, Large Language Models and prompt engineering techniques, Cloud-based AI services and integration, Software development lifecycle and version control\"\n",
    "top_docs = mock_vector_search(focus_areas_query, top_k=5)\n"
   ]
  }
]

# Chèn cell vào sau Bước 6 (Interview Prepare)
insert_index = 0
for i, cell in enumerate(nb['cells']):
    if "## 7. Interview Prepare" in "".join(cell.get('source', [])):
        insert_index = i
        break

if insert_index > 0:
    nb['cells'] = nb['cells'][:insert_index] + new_cells + nb['cells'][insert_index:]
else:
    nb['cells'].extend(new_cells)

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Added RAG vector search mock to notebook.")
