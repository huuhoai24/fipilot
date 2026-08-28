import os
import glob
import logging
from typing import List
from pathlib import Path
import numpy as np

from infrastructure.llm.base import BaseLLMService

logger = logging.getLogger(__name__)

class RagRetrieverMock:
    def __init__(self, llm_service: BaseLLMService, processed_dir: str = None):
        self.llm_service = llm_service
        
        if not processed_dir:
            base_path = Path(__file__).parent.parent.parent
            self.processed_dir = str(base_path / "data" / "processed")
        else:
            self.processed_dir = processed_dir
            
        self.doc_contents: List[str] = []
        self.doc_embeddings = None
        
        # Load pre-processed embeddings
        self._load_embeddings()

    def _load_embeddings(self):
        """Loads pre-processed .npz embedding files from data/processed."""
        if not os.path.exists(self.processed_dir):
            logger.warning(f"Processed directory not found: {self.processed_dir}")
            return
            
        search_pattern = f"{self.processed_dir}/domain_index_*.npz"
        npz_files = glob.glob(search_pattern)
        
        all_embeddings = []
        all_paths_and_content = []
        
        for file in npz_files:
            try:
                data = np.load(file, allow_pickle=True)
                all_embeddings.append(data['embeddings'])
                all_paths_and_content.extend(data['paths'])
            except Exception as e:
                logger.error(f"Failed to load {file}: {e}")
                
        if all_embeddings:
            self.doc_embeddings = np.vstack(all_embeddings)
            self.doc_contents = all_paths_and_content
            logger.info(f"Loaded {len(self.doc_contents)} document embeddings from {len(npz_files)} domains.")
        else:
            logger.warning("No pre-computed embeddings found.")

    def _cosine_similarity(self, query_vec, doc_matrix):
        """Computes cosine similarity between query vector (1D) and document matrix (2D)."""
        # query_vec: (D,)
        # doc_matrix: (N, D)
        query_vec = np.array(query_vec)
        dot_products = np.dot(doc_matrix, query_vec)
        norm_query = np.linalg.norm(query_vec)
        norms_docs = np.linalg.norm(doc_matrix, axis=1)
        
        # Avoid division by zero
        norms = norm_query * norms_docs
        norms[norms == 0] = 1e-10
        
        return dot_products / norms

    async def retrieve(self, query: str, top_k: int = 3) -> str:
        """
        Retrieves the top_k most relevant documents for the given query using Azure OpenAI embeddings.
        """
        if not self.doc_contents or self.doc_embeddings is None:
            return "No background knowledge available (npz files not loaded)."
            
        try:
            # Generate embedding for the query using Azure OpenAI
            query_embedding = await self.llm_service.generate_embedding(query)
            
            # Compute cosine similarities using NumPy (much faster)
            similarities = self._cosine_similarity(query_embedding, self.doc_embeddings)
            
            # Get indices of top_k results
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                score = similarities[idx]
                if score > 0.3: # Threshold
                    # Content format in npz is usually "Path\nContent"
                    raw_content = self.doc_contents[idx]
                    parts = raw_content.split('\n', 1)
                    doc_name = parts[0] if len(parts) > 1 else f"Doc_{idx}"
                    doc_text = parts[1] if len(parts) > 1 else raw_content
                    
                    results.append(f"--- Document: {doc_name} (Similarity: {score:.4f}) ---\n{doc_text}\n")
                    
            if not results:
                return "No highly relevant background knowledge found for this query."
                
            return "\n".join(results)
            
        except Exception as e:
            logger.error(f"Error during RAG retrieval: {e}")
            return "Error retrieving knowledge."

    async def retrieve_for_focus_areas(self, focus_areas: List[str], top_k: int = 3) -> str:
        query = ", ".join(focus_areas)
        return await self.retrieve(query, top_k)
