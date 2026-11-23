from .data_pipeline import DataPipeline


class APIPipeline(DataPipeline):
    name = "API"
    required_fields = ("user_id", "username")
    GRADE_A_THRESHOLD = 90

    def extract(self) -> list[dict]:
        return [
            {"user_id": 101, "username": "Charlie", "score": "85"},
            {"user_id": 102, "username": "Diana", "score": "92"},
        ]

    def transform_record(self, record: dict) -> dict:
        score = int(record["score"])
        return {
            **record,
            "score": score,
            "username": record["username"].lower(),
            "grade": "A" if score >= self.GRADE_A_THRESHOLD else "B",
        }
