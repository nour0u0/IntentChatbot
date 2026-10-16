
import json
from pathlib import Path

from sentence_transformers import SentenceTransformer

from Model.Question import Question
from Model.AnswerEmbed import AnswerEmbed



class RegisterService:
    MODEL_DIR = (
        Path(__file__).resolve().parent
        /".."
        / "models"
        / "all-MiniLM-L6-v2"
    )

    def __init__(self):
        if not self.MODEL_DIR.exists():
            raise FileNotFoundError(
                f"Local embedding model not found: {self.MODEL_DIR}"
            )

        self.model = SentenceTransformer(str(self.MODEL_DIR))

    def _next_id(self):
        records = Question._load_all()

        if not records:
            return 1

        return max(record["QuestionId"] for record in records) + 1

    def register(self, json_file):
        json_file = Path(json_file)

        with json_file.open("r", encoding="utf-8") as file:
            data = json.load(file)

        # Accept either one object or a list of objects.
        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list):
            raise ValueError(
                "JSON must contain an object or a list of objects."
            )

        results = []

        for index, item in enumerate(data):
            if not isinstance(item, dict):
                raise ValueError(
                    f"Item {index} must be a JSON object."
                )

            question_text = item.get("Question")
            answer_text = item.get("Answer")

            if not isinstance(question_text, str) or not question_text.strip():
                raise ValueError(
                    f"Item {index}: Question must be a non-empty string."
                )

            if not isinstance(answer_text, str) or not answer_text.strip():
                raise ValueError(
                    f"Item {index}: Answer must be a non-empty string."
                )

            question_text = question_text.strip()
            answer_text = answer_text.strip()

            question_id = self._next_id()

            embedding = self.model.encode(
                question_text,
                convert_to_numpy=True,
                normalize_embeddings=True
            )

            Question(
                question_id,
                question_text
            ).save()

            AnswerEmbed(
                question_id,
                answer_text,
                embedding
            ).save()

            results.append({
                "question_id": question_id,
                "question": question_text,
                "answer": answer_text
            })

        return results
