"""Quiz and Assessment App - core quiz logic.

This module contains all reusable business logic for loading, validating,
scoring and reviewing quiz questions. It is intentionally independent of
Flask so it can be unit-tested in isolation.
"""

import json
import os

# Path to the default questions file, relative to this module.
DEFAULT_QUESTIONS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "questions.json"
)

REQUIRED_FIELDS = ("id", "question", "options", "answer", "explanation")
MIN_OPTIONS = 2
MAX_OPTIONS = 6


# ---------------------------------------------------------------------------
# Loading & validation
# ---------------------------------------------------------------------------

def load_questions(path=DEFAULT_QUESTIONS_PATH):
    """Load and validate questions from a JSON file.

    Returns a tuple (questions, error):
      - questions: list of validated question dicts (empty on failure)
      - error: human-friendly error message, or None on success
    """
    if not os.path.exists(path):
        return [], f"Questions file not found: {os.path.basename(path)}"

    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = fh.read()
    except OSError as exc:
        return [], f"Could not read questions file: {exc}"

    if not raw.strip():
        return [], "Questions file is empty."

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return [], f"Invalid JSON in questions file: {exc.msg} (line {exc.lineno})"

    return validate_questions(data)


def validate_questions(data):
    """Validate the decoded JSON structure for the quiz.

    Returns (questions, error).
    """
    if not isinstance(data, list):
        return [], "Questions file must contain a JSON array of questions."

    if not data:
        return [], "Questions file contains no questions."

    seen_ids = set()
    questions = []

    for index, item in enumerate(data, start=1):
        label = f"Question #{index}"
        qid = item.get("id") if isinstance(item, dict) else None
        if isinstance(qid, int):
            label = f"Question ID {qid}"

        if not isinstance(item, dict):
            return [], f"{label}: entry must be a JSON object."

        for field in REQUIRED_FIELDS:
            if field not in item:
                return [], f"{label}: missing required field '{field}'."

        qid = item["id"]
        if not isinstance(qid, int) or isinstance(qid, bool):
            return [], f"{label}: 'id' must be an integer."
        if qid in seen_ids:
            return [], f"{label}: duplicate question ID {qid}."
        seen_ids.add(qid)

        if not isinstance(item["question"], str) or not item["question"].strip():
            return [], f"{label}: 'question' must be a non-empty string."

        options = item["options"]
        if not isinstance(options, list) or not (
            MIN_OPTIONS <= len(options) <= MAX_OPTIONS
        ):
            return [], (
                f"{label}: 'options' must be a list of "
                f"{MIN_OPTIONS}-{MAX_OPTIONS} choices."
            )
        if any(not isinstance(o, str) or not o.strip() for o in options):
            return [], f"{label}: every option must be a non-empty string."
        if len(set(options)) != len(options):
            return [], f"{label}: 'options' contains duplicate choices."

        answer = item["answer"]
        if not isinstance(answer, str) or not answer.strip():
            return [], f"{label}: 'answer' must be a non-empty string."
        if answer not in options:
            return [], (
                f"{label}: 'answer' must exactly match one of the options."
            )

        if not isinstance(item["explanation"], str) or not item["explanation"].strip():
            return [], f"{label}: 'explanation' must be a non-empty string."

        questions.append(
            {
                "id": qid,
                "question": item["question"],
                "options": list(options),
                "answer": answer,
                "explanation": item["explanation"],
            }
        )

    return questions, None


def public_questions(questions):
    """Return question data safe to send to the client (no answers)."""
    return [
        {
            "id": q["id"],
            "question": q["question"],
            "options": list(q["options"]),
        }
        for q in questions
    ]


# ---------------------------------------------------------------------------
# Submission validation & scoring
# ---------------------------------------------------------------------------

def normalize_answers(payload):
    """Extract the answers dict from a submission payload.

    Returns (answers, error). answers maps str(question_id) -> str(option).
    """
    if not isinstance(payload, dict):
        return None, "Request body must be a JSON object."

    answers = payload.get("answers")
    if answers is None:
        return {}, None  # treat missing 'answers' as all unanswered
    if not isinstance(answers, dict):
        return None, "'answers' must be an object mapping question IDs to choices."

    clean = {}
    for key, value in answers.items():
        if isinstance(value, str) and value.strip():
            clean[str(key)] = value.strip()
        # empty/blank values are ignored (treated as unanswered)
    return clean, None


def score_submission(questions, answers):
    """Score a submission.

    answers: dict mapping str(question_id) -> selected option string.
    Returns a results dict with score, percentage, feedback and review.
    """
    total = len(questions)
    correct_count = 0
    review = []

    for q in questions:
        qid = str(q["id"])
        selected = answers.get(qid)
        is_correct = selected is not None and selected == q["answer"]
        if is_correct:
            correct_count += 1

        review.append(
            {
                "id": q["id"],
                "question": q["question"],
                "options": list(q["options"]),
                "selected": selected,
                "correct_answer": q["answer"],
                "is_correct": is_correct,
                "explanation": q["explanation"],
            }
        )

    incorrect_count = total - correct_count - sum(
        1 for r in review if r["selected"] is None
    )
    unanswered_count = sum(1 for r in review if r["selected"] is None)

    percentage = round((correct_count / total) * 100, 2) if total else 0.0

    return {
        "total_questions": total,
        "correct_answers": correct_count,
        "incorrect_answers": incorrect_count,
        "unanswered": unanswered_count,
        "score": f"{correct_count}/{total}",
        "percentage": percentage,
        "feedback": get_feedback(percentage),
        "review": review,
    }


def get_feedback(percentage):
    """Return performance feedback for a percentage score."""
    if percentage >= 80:
        return "Excellent work!"
    if percentage >= 50:
        return "Good job, keep improving!"
    return "Keep practicing, you can do better!"
