from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import glob
from pathlib import Path

def mock_vector_search(query: str, top_k: int = 3):
    knowledge_dir = str(Path(os.getcwd()) / "Knowledge" / "Domains" / "AI_Enginner")
    search_patterns = [f"{knowledge_dir}/**/*.md"]
    
    doc_paths = []
    for pattern in search_patterns:
        doc_paths.extend(glob.glob(pattern, recursive=True))
        
    documents = []
    doc_names = []
    for path in doc_paths:
        with open(path, 'r', encoding='utf-8') as f:
            documents.append(f.read())
            doc_names.append("/".join(path.split(os.sep)[-2:]))
            
    vectorizer = TfidfVectorizer(stop_words='english')
    all_texts = [query] + documents
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    top_indices = cosine_similarities.argsort()[-top_k:][::-1]
    
    print("===============================================")
    print("[INPUT QUERY]:")
    print(f"> {query}\n")
    print("[TOP KẾT QUẢ VECTOR SEARCH]: ")
    
    for i, idx in enumerate(top_indices):
        score = cosine_similarities[idx]
        print(f"{i+1}. Document: {doc_names[idx]}")
        print(f"   - Similarity Score: {score:.4f}")

query = "Computer Vision model development and optimization, Deep Learning frameworks usage and deployment, Large Language Models and prompt engineering techniques, Cloud-based AI services and integration, Software development lifecycle and version control"
mock_vector_search(query, top_k=5)
