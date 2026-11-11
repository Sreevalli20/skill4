"""Automated tests for the Quiz and Assessment App.

Run from the quiz-app directory:
    python -m unittest discover -s tests -v
"""

import json
import os
import sys
import tempfile
import unittest

# Make the quiz-app package importable when running from tests/.
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, APP_DIR)

import quiz_logic  # noqa: E402
from app import app  # noqa: E402


SAMPLE_QUESTIONS = [
    {
        "id": 1,
        "question": "Q1?",
        "options": ["a", "b", "c", "d"],
        "answer": "a",
        "explanation": "Because a.",
    },
    {
        "id": 2,
        "question": "Q2?",
        "options": ["w", "x", "y", "z"],
        "answer": "y",
        "explanation": "Because y.",
    },
]


def write_temp_json(data):
    """Write data (str or object) to a temp JSON file; return its path."""
    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        if isinstance(data, str):
            fh.write(data)
        else:
            json.dump(data, fh)
    return path


class QuestionLoadingTests(unittest.TestCase):
    """Tests for load_questions / validate_questions."""

    def test_load_valid_file(self):
        path = write_temp_json(SAMPLE_QUESTIONS)
        try:
            questions, error = quiz_logic.load_questions(path)
            self.assertIsNone(error)
            self.assertEqual(len(questions), 2)
            self.assertEqual(questions[0]["answer"], "a")
        finally:
            os.remove(path)

    def test_load_default_questions_file(self):
        questions, error = quiz_logic.load_questions()
        self.assertIsNone(error)
        self.assertEqual(len(questions), 10)

    def test_missing_file(self):
        questions, error = quiz_logic.load_questions("does_not_exist.json")
        self.assertEqual(questions, [])
        self.assertIn("not found", error.lower())

    def test_empty_file(self):
        path = write_temp_json("")
        try:
            questions, error = quiz_logic.load_questions(path)
            self.assertEqual(questions, [])
            self.assertIn("empty", error.lower())
        finally:
            os.remove(path)

    def test_malformed_json(self):
        path = write_temp_json("{not valid json")
        try:
            questions, error = quiz_logic.load_questions(path)
            self.assertEqual(questions, [])
            self.assertIn("invalid json", error.lower())
        finally:
            os.remove(path)

    def test_missing_field(self):
        bad = [dict(SAMPLE_QUESTIONS[0])]
        del bad[0]["answer"]
        questions, error = quiz_logic.validate_questions(bad)
        self.assertEqual(questions, [])
        self.assertIn("answer", error)

    def test_duplicate_ids(self):
        bad = [dict(SAMPLE_QUESTIONS[0]), dict(SAMPLE_QUESTIONS[0])]
        questions, error = quiz_logic.validate_questions(bad)
        self.assertEqual(questions, [])
        self.assertIn("duplicate", error.lower())

    def test_answer_not_in_options(self):
        bad = [dict(SAMPLE_QUESTIONS[0], answer="not-an-option")]
        questions, error = quiz_logic.validate_questions(bad)
        self.assertEqual(questions, [])
        self.assertIn("answer", error.lower())

    def test_duplicate_options(self):
        bad = [
            dict(SAMPLE_QUESTIONS[0], options=["a", "a", "b", "c"])
        ]
        questions, error = quiz_logic.validate_questions(bad)
        self.assertEqual(questions, [])
        self.assertIn("duplicate", error.lower())

    def test_wrong_data_types(self):
        bad = [dict(SAMPLE_QUESTIONS[0], id="one")]
        questions, error = quiz_logic.validate_questions(bad)
        self.assertEqual(questions, [])
        self.assertIn("id", error.lower())

    def test_public_questions_hide_answers(self):
        public = quiz_logic.public_questions(SAMPLE_QUESTIONS)
        for q in public:
            self.assertNotIn("answer", q)
            self.assertNotIn("explanation", q)


class ScoringTests(unittest.TestCase):
    """Tests for scoring, percentage and feedback."""

    def _questions(self, n=10):
        return [
            {
                "id": i,
                "question": f"Q{i}?",
                "options": ["a", "b"],
                "answer": "a",
                "explanation": "x",
            }
            for i in range(1, n + 1)
        ]

    def test_all_correct(self):
        questions = self._questions(10)
        answers = {str(i): "a" for i in range(1, 11)}
        result = quiz_logic.score_submission(questions, answers)
        self.assertEqual(result["correct_answers"], 10)
        self.assertEqual(result["score"], "10/10")
        self.assertEqual(result["percentage"], 100.0)
        self.assertEqual(result["feedback"], "Excellent work!")

    def test_all_incorrect(self):
        questions = self._questions(10)
        answers = {str(i): "b" for i in range(1, 11)}
        result = quiz_logic.score_submission(questions, answers)
        self.assertEqual(result["correct_answers"], 0)
        self.assertEqual(result["percentage"], 0.0)
        self.assertEqual(result["feedback"], "Keep practicing, you can do better!")

    def test_feedback_boundaries(self):
        self.assertEqual(quiz_logic.get_feedback(100), "Excellent work!")
        self.assertEqual(quiz_logic.get_feedback(80), "Excellent work!")
        self.assertEqual(quiz_logic.get_feedback(79.9), "Good job, keep improving!")
        self.assertEqual(quiz_logic.get_feedback(70), "Good job, keep improving!")
        self.assertEqual(quiz_logic.get_feedback(50), "Good job, keep improving!")
        self.assertEqual(quiz_logic.get_feedback(49.9), "Keep practicing, you can do better!")
        self.assertEqual(quiz_logic.get_feedback(0), "Keep practicing, you can do better!")

    def test_partial_score_70_percent(self):
        questions = self._questions(10)
        answers = {str(i): "a" for i in range(1, 8)}
        answers.update({str(i): "b" for i in range(8, 11)})
        result = quiz_logic.score_submission(questions, answers)
        self.assertEqual(result["percentage"], 70.0)
        self.assertEqual(result["feedback"], "Good job, keep improving!")

    def test_all_unanswered(self):
        questions = self._questions(10)
        result = quiz_logic.score_submission(questions, {})
        self.assertEqual(result["correct_answers"], 0)
        self.assertEqual(result["unanswered"], 10)
        self.assertEqual(result["incorrect_answers"], 0)
        self.assertEqual(result["percentage"], 0.0)

    def test_partially_unanswered(self):
        questions = self._questions(10)
        answers = {str(i): "a" for i in range(1, 6)}  # 5 correct, 5 unanswered
        answers["6"] = "b"  # 1 incorrect
        result = quiz_logic.score_submission(questions, answers)
        self.assertEqual(result["correct_answers"], 5)
        self.assertEqual(result["incorrect_answers"], 1)
        self.assertEqual(result["unanswered"], 4)
        self.assertEqual(result["percentage"], 50.0)
        self.assertEqual(result["feedback"], "Good job, keep improving!")

    def test_review_contains_expected_fields(self):
        questions = self._questions(2)
        result = quiz_logic.score_submission(questions, {"1": "a", "2": "b"})
        self.assertEqual(len(result["review"]), 2)
        first = result["review"][0]
        for field in ("id", "question", "options", "selected",
                      "correct_answer", "is_correct", "explanation"):
            self.assertIn(field, first)
        self.assertTrue(first["is_correct"])
        self.assertFalse(result["review"][1]["is_correct"])


class ApiTests(unittest.TestCase):
    """Tests for the Flask routes using the test client."""

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_home_route(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Quiz", res.data)

    def test_questions_api(self):
        res = self.client.get("/api/questions")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("questions", data)
        self.assertEqual(len(data["questions"]), 10)

    def test_questions_api_hides_answers(self):
        res = self.client.get("/api/questions")
        data = res.get_json()
        for q in data["questions"]:
            self.assertNotIn("answer", q)
            self.assertNotIn("explanation", q)

    def _correct_answers(self):
        questions, error = quiz_logic.load_questions()
        self.assertIsNone(error)
        return {str(q["id"]): q["answer"] for q in questions}

    def test_submit_all_correct(self):
        res = self.client.post("/api/submit", json={"answers": self._correct_answers()})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["score"], "10/10")
        self.assertEqual(data["percentage"], 100.0)
        self.assertEqual(data["feedback"], "Excellent work!")

    def test_submit_all_wrong(self):
        # Pick a wrong option for each question.
        questions, _ = quiz_logic.load_questions()
        answers = {
            str(q["id"]): next(o for o in q["options"] if o != q["answer"])
            for q in questions
        }
        res = self.client.post("/api/submit", json={"answers": answers})
        data = res.get_json()
        self.assertEqual(data["correct_answers"], 0)
        self.assertEqual(data["percentage"], 0.0)

    def test_submit_unanswered(self):
        res = self.client.post("/api/submit", json={"answers": {}})
        data = res.get_json()
        self.assertEqual(data["unanswered"], 10)
        self.assertEqual(data["percentage"], 0.0)

    def test_invalid_question_id(self):
        res = self.client.post(
            "/api/submit", json={"answers": {"999": "def"}}
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn("error", res.get_json())

    def test_invalid_answer_value(self):
        res = self.client.post(
            "/api/submit", json={"answers": {"1": "not-a-real-option"}}
        )
        self.assertEqual(res.status_code, 400)

    def test_invalid_submission_body(self):
        res = self.client.post(
            "/api/submit",
            data="not json",
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 400)

    def test_missing_answers_field(self):
        res = self.client.post("/api/submit", json={})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["unanswered"], 10)

    def test_repeated_submission_is_stateless(self):
        answers = self._correct_answers()
        res1 = self.client.post("/api/submit", json={"answers": answers})
        res2 = self.client.post("/api/submit", json={"answers": answers})
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res1.get_json()["score"], res2.get_json()["score"])


if __name__ == "__main__":
    unittest.main()
