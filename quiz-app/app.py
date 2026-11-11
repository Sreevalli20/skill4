"""Quiz and Assessment App - Flask backend.

Routes:
  GET  /            -> serves the quiz frontend
  GET  /api/questions -> questions without correct answers
  POST /api/submit    -> validates answers, scores and returns review
"""

import os

from flask import Flask, jsonify, request, send_from_directory

import quiz_logic

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
QUESTIONS_PATH = quiz_logic.DEFAULT_QUESTIONS_PATH

app = Flask(__name__)


def load_or_error():
    """Load questions; return (questions, error_response)."""
    questions, error = quiz_logic.load_questions(QUESTIONS_PATH)
    if error:
        return None, (jsonify({"error": error}), 500)
    return questions, None


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


@app.route("/api/questions")
def api_questions():
    questions, err = load_or_error()
    if err:
        return err
    return jsonify({"questions": quiz_logic.public_questions(questions)})


@app.route("/api/submit", methods=["POST"])
def api_submit():
    questions, err = load_or_error()
    if err:
        return err

    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    answers, err_msg = quiz_logic.normalize_answers(payload)
    if err_msg:
        return jsonify({"error": err_msg}), 400

    # Map valid question IDs for validation.
    valid_ids = {str(q["id"]) for q in questions}
    option_lookup = {
        str(q["id"]): set(q["options"]) for q in questions
    }

    for qid, value in answers.items():
        if qid not in valid_ids:
            return jsonify(
                {"error": f"Invalid question ID: {qid}."}
            ), 400
        if value not in option_lookup[qid]:
            return jsonify(
                {"error": f"Invalid answer for question {qid}."}
            ), 400

    results = quiz_logic.score_submission(questions, answers)
    return jsonify(results)


@app.errorhandler(404)
def not_found(_exc):
    return jsonify({"error": "Not found."}), 404


@app.errorhandler(500)
def server_error(_exc):
    return jsonify({"error": "An unexpected server error occurred."}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
