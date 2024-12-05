from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

class VectorStore:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.embedder = SentenceTransformer(model_name)
        self.documents = []
        self.embeddings = np.array([])
        self.chunks = []

    def add_document(self, document, chunk_size=500, overlap=50):
        chunks = self._chunk_text(document.content, chunk_size, overlap)
        if not chunks:
            return False

        embeddings = self.embedder.encode(chunks)
        document.chunks = chunks
        document.embeddings = embeddings
        self.documents.append(document)
        self.chunks.extend(chunks)

        if self.embeddings.size == 0:
            self.embeddings = embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, embeddings])
        return True

    def search(self, query: str, k: int = 3) -> List[str]:
        if not self.chunks:
            return []

        query_embedding = self.embedder.encode([query])[0]
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        top_k_indices = np.argsort(similarities)[-k:][::-1]
        return [self.chunks[i] for i in top_k_indices]

    def _chunk_text(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        if not text.strip():
            return []

        chunks = []
        start = 0
        text = text.strip()

        while start < len(text):
            end = start + chunk_size
            if end > len(text):
                end = len(text)
            else:
                last_period = text.rfind('.', start, end)
                last_newline = text.rfind('\n', start, end)
                break_point = max(last_period, last_newline)
                if break_point > start:
                    end = break_point + 1

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start += chunk_size - overlap

        return chunks

    def has_documents(self):
        return len(self.documents) > 0

    def reset(self):
        self.documents = []
        self.embeddings = np.array([])
        self.chunks = []