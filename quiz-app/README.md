# Quiz & Assessment App

A professional, responsive web-based quiz application built with **Python 3.14.6**, **Flask**, **HTML5**, **CSS3**, and **JavaScript**. The quiz topic is *Python Programming Basics* — 10 multiple-choice questions stored in a JSON file so questions can be updated without touching any code.

## Features

- Start screen with quiz info and question count
- Multiple-choice quiz with one answer per question
- Question navigation (Previous / Next) and live progress indicator
- Warning before submitting with unanswered questions (with quick jump to the first unanswered question)
- Automatic scoring: 1 mark per correct answer, no negative marking
- Percentage score and performance feedback (Excellent / Good / Keep practicing)
- Full answer review with correct answers and explanations
- Retry quiz with fully reset state
- Duplicate-submission protection
- Friendly error handling for missing/invalid question data — no tracebacks
- Fully responsive design (desktop, laptop, tablet, mobile)
- No external APIs, API keys, or third-party dependencies

## Technology Stack

| Layer    | Technology                          |
|----------|-------------------------------------|
| Backend  | Python 3.14.6, Flask 3.0.3          |
| Data     | JSON (`data/questions.json`)        |
| Frontend | HTML5, CSS3, Vanilla JavaScript     |
| Testing  | `unittest` + Flask test client      |

## Project Structure

```
quiz-app/
├── app.py                  # Flask routes (/ , /api/questions, /api/submit)
├── quiz_logic.py           # Question loading, validation, scoring, feedback
├── requirements.txt        # Flask==3.0.3
├── README.md
├── .gitignore
├── frontend/
│   ├── index.html          # Start / quiz / result / review screens
│   ├── style.css           # Responsive styling
│   └── script.js           # Quiz interactions (fetch, navigation, submit)
├── data/
│   └── questions.json      # 10 MCQ questions with answers & explanations
├── tests/
│   ├── __init__.py
│   ├── test_quiz.py        # 29 automated tests
│   └── test_cases.md       # Manual test report
└── screenshots/            # Place app screenshots here
```

## Requirements

- **Python 3.14.6** (verified: `python --version`)
- Flask 3.0.3 (compatible with Python 3.14)

## Installation

```bash
cd quiz-app
python -m pip install -r requirements.txt
```

## Running the Application

```bash
cd quiz-app
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## API Endpoints

| Method | Endpoint         | Description                                        |
|--------|------------------|----------------------------------------------------|
| GET    | `/`              | Serves the quiz frontend                          |
| GET    | `/api/questions` | Returns questions **without** correct answers     |
| POST   | `/api/submit`    | Body: `{"answers": {"<id>": "<option>"}}` — returns score, percentage, feedback, and per-question review |

Example submission:

```bash
curl -X POST http://127.0.0.1:5000/api/submit \
  -H "Content-Type: application/json" \
  -d '{"answers": {"1": "def", "2": "print(\"Hello, World!\")"}}'
```

## Scoring Rules

- 1 mark per correct answer, 0 for incorrect — no negative marking.
- Unanswered questions count as incorrect.
- `percentage = (correct / total) * 100`
- Feedback: **≥ 80%** → "Excellent work!" · **50–79%** → "Good job, keep improving!" · **< 50%** → "Keep practicing, you can do better!"

## Question JSON Format

Each question in `data/questions.json`:

```json
{
  "id": 1,
  "question": "Which keyword is used to define a function in Python?",
  "options": ["func", "def", "function", "define"],
  "answer": "def",
  "explanation": "Python uses the def keyword to define a function."
}
```

Validation rejects: missing files, empty/malformed JSON, missing fields,
duplicate IDs or options, answers not matching an option, and wrong data types — all reported as friendly error messages.

## Running Tests

```bash
cd quiz-app
python -m unittest discover -s tests -v
```

29 tests covering question loading/validation, scoring boundaries,
percentage/feedback rules, and all API routes.

## Screenshots

Add screenshots of the start, quiz, result, and review screens to the
`screenshots/` folder (see `screenshots/README.md` for filenames).

## Limitations

- Single fixed quiz (10 questions, Python basics); no categories or difficulty levels.
- No user accounts, score persistence, or server-side sessions.
- Unanswered-submission warning uses the browser's native `confirm()` dialog.

## Repository

https://github.com/Sreevalli20/skill4
