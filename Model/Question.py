
import json
from pathlib import Path


class Question:
    DB_FILE = Path(__file__).resolve().parent / ".."/"DB" / "Question.json"

    def __init__(self, ID, Question: str):
        self.QuestionId = ID
        self.Text = Question

    @classmethod
    def _load_all(cls):
        cls.DB_FILE.parent.mkdir(parents=True, exist_ok=True)

        if not cls.DB_FILE.exists():
            return []

        with cls.DB_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)

    @classmethod
    def _write_all(cls, records):
        cls.DB_FILE.parent.mkdir(parents=True, exist_ok=True)

        with cls.DB_FILE.open("w", encoding="utf-8") as file:
            json.dump(records, file, indent=4, ensure_ascii=False)

    def save(self):
        records = self._load_all()

        record = {
            "QuestionId": self.QuestionId,
            "Text": self.Text
        }

        for index, existing in enumerate(records):
            if existing["QuestionId"] == self.QuestionId:
                records[index] = record
                break
        else:
            records.append(record)

        self._write_all(records)
        return self

    @classmethod
    def get(cls, QuestionId):
        for record in cls._load_all():
            if record["QuestionId"] == QuestionId:
                return cls(
                    ID=record["QuestionId"],
                    Question=record["Text"]
                )

        return None

    @classmethod
    def delete(cls, QuestionId):
        records = cls._load_all()
        updated = [
            record for record in records
            if record["QuestionId"] != QuestionId
        ]

        if len(updated) == len(records):
            return False

        cls._write_all(updated)
        return True
