
import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

from Model.Question import Question
from Model.AnswerEmbed import AnswerEmbed


class ChatService:
    MODEL_DIR = (
        Path(__file__).resolve().parent
        /".."
        / "models"
        / "all-MiniLM-L6-v2"
    )

    def __init__(self, threshold=0.60):
        if not self.MODEL_DIR.exists():
            raise FileNotFoundError(
                f"Local embedding model not found: {self.MODEL_DIR}"
            )

        self.model = SentenceTransformer(str(self.MODEL_DIR))
        self.threshold = threshold

    def _embed(self, text):
        return self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype(np.float32)

    def _cosine_similarity(self, a, b):
        # Embeddings are normalized, so cosine similarity is their dot product.
        return float(np.dot(a, b))

    def respond(self, prompt):
        if not isinstance(prompt, str) or not prompt.strip():
            return None

        prompt_embedding = self._embed(prompt.strip())

        best_answer = None
        best_score = -1.0

        # Iterate through stored questions.
        for record in Question._load_all():
            question_id = record["QuestionId"]
            stored_question = record["Text"]

            answer = AnswerEmbed.get(question_id)

            if answer is None:
                continue

            stored_embedding = answer.Questionembedding

            if stored_embedding.shape != prompt_embedding.shape:
                continue

            score = self._cosine_similarity(
                prompt_embedding,
                stored_embedding
            )

            if score > best_score:
                best_score = score
                best_answer = answer

        if best_answer is None or best_score < self.threshold:
            return None

        return {
            "answer": best_answer.Text,
            "question_id": best_answer.QuestionId,
            "similarity": best_score
        }
