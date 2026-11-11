
# Quiz and Assessment App

**Python Programming – Week 4 | Intermediate Level Project**

## 1. Project Overview

The Quiz and Assessment App is a web-based application developed using Python and Flask. It allows users to answer multiple-choice questions, submit their responses, and instantly view their quiz results.

The application automatically checks answers, calculates scores and percentages, and provides performance-based feedback.

Users can also review correct and incorrect answers along with explanations.

Quiz questions are stored in a JSON file, making it easy to add, remove, or update questions without modifying the application logic.

## 2. Features

- Interactive multiple-choice quiz.
- 10 Python programming questions.
- Four options for each question.
- One answer selection per question.
- Previous and Next question navigation.
- Question progress indicator.
- Unanswered question validation.
- Automatic answer checking.
- Instant score calculation.
- Percentage calculation.
- Performance-based feedback.
- Correct and incorrect answer review.
- Explanations for every question.
- Retry quiz functionality.
- Responsive user interface.
- JSON-based question storage.
- Backend answer validation.
- Error handling for invalid or missing question data.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.14.6 | Backend programming |
| Flask | Web application framework |
| HTML5 | Application structure |
| CSS3 | User interface styling |
| JavaScript | Frontend interactions |
| JSON | Question data storage |
| unittest | Automated testing |
| Git and GitHub | Version control |

No external API key or paid API service is required.

## 4. Project Structure

```text
quiz-app/
│
├── app.py
├── quiz_logic.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── data/
│   └── questions.json
│
├── tests/
│   ├── __init__.py
│   ├── test_quiz.py
│   └── test_cases.md
│
└── screenshots/
```

## 5. Quiz Scoring System

The application uses the following scoring rules:

- Each correct answer receives 1 mark.
- Incorrect answers receive 0 marks.
- Unanswered questions receive 0 marks.
- No negative marking.
- Maximum score is 10.

### Percentage Formula

Percentage = (Correct Answers / Total Questions) × 100

### Performance Feedback

| Percentage | Feedback |
|---|---|
| 80% – 100% | Excellent work! |
| 50% – 79% | Good job, keep improving! |
| Below 50% | Keep practicing, you can do better! |

### Example Results

| Score | Percentage | Feedback |
|---|---|---|
| 10/10 | 100% | Excellent work! |
| 8/10 | 80% | Excellent work! |
| 7/10 | 70% | Good job, keep improving! |
| 5/10 | 50% | Good job, keep improving! |
| 3/10 | 30% | Keep practicing, you can do better! |
| 0/10 | 0% | Keep practicing, you can do better! |

## 6. Question Data Storage

Quiz questions are stored in:

`data/questions.json`

Each question contains:

- Unique question ID.
- Question text.
- Four answer options.
- Correct answer.
- Explanation.

### Example JSON Format

```json
{
  "id": 1,
  "question": "Which keyword is used to define a function in Python?",
  "options": [
    "func",
    "def",
    "function",
    "define"
  ],
  "answer": "def",
  "explanation": "Python uses the def keyword to define a function."
}
```

Questions can be updated directly in the JSON file without changing the scoring logic.

Correct answers are validated by the Python backend and are not included in the public questions API response.

## 7. Requirements

- Python 3.14.6
- Flask compatible with Python 3.14.6
- Modern web browser
- Terminal or command prompt

Verify your Python installation:

```bash
python --version
```

Expected output:

```text
Python 3.14.6
```

## 8. Installation

### Step 1: Clone the GitHub Repository

```bash
git clone https://github.com/Sreevalli20/skill4.git
```

### Step 2: Navigate to the Project Directory

```bash
cd skill4/quiz-app
```

### Step 3: Create a Virtual Environment (Optional)

```bash
python -m venv .venv
```

Activate on Windows:

```bash
.venv\Scripts\activate
```

Activate on macOS or Linux:

```bash
source .venv/bin/activate
```

### Step 4: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

The requirements file should contain only the verified Flask dependency needed by the application.

## 9. Running the Application

Start the Flask application:

```bash
python app.py
```

Open your browser and visit:

http://127.0.0.1:5000/

To stop the application, press `Ctrl + C` in the terminal.

## 10. Application Workflow

1. Open the application in a web browser.
2. View the quiz introduction.
3. Click the Start Quiz button.
4. Read the displayed question.
5. Select one answer from the available options.
6. Navigate using Previous and Next buttons.
7. Review unanswered questions.
8. Submit the completed quiz.
9. View the final score and percentage.
10. Review correct and incorrect answers.
11. Read the explanations.
12. Click Retry Quiz to attempt the quiz again.

## 11. Backend API Routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Display the quiz application |
| `/api/questions` | GET | Retrieve questions without correct answers |
| `/api/submit` | POST | Validate answers and calculate results |

The backend validates submitted answers and calculates scores.

## 12. Testing

The application uses Python's built-in `unittest` framework for automated testing.

Run automated tests from the quiz-app directory:

```bash
python -m unittest discover -s tests -v
```

The automated tests cover:

- Question loading.
- Correct answer validation.
- Incorrect answer validation.
- Score calculation.
- Percentage calculation.
- Performance feedback.
- Unanswered questions.
- Invalid question IDs.
- Invalid answer options.
- Missing JSON files.
- Empty JSON files.
- Malformed JSON.
- Duplicate question IDs.
- Flask routes.
- API responses.
- Invalid submissions.
- Correct answer confidentiality.

Manual test cases and actual test results are documented in:

`tests/test_cases.md`

## 13. Screenshots

The `screenshots/` directory is provided to store genuine application screenshots.

Capture the following after running the application:

1. Quiz start page.
2. Quiz question page.
3. Quiz result page.
4. Answer review page.

Only actual application screenshots should be included.

## 14. Error Handling

The application handles common errors, including:

- Missing question files.
- Empty JSON files.
- Invalid JSON formatting.
- Missing question fields.
- Invalid answer selections.
- Invalid question IDs.
- Unanswered questions.
- Failed network requests.
- Unexpected backend errors.

Friendly error messages are displayed instead of exposing internal application tracebacks.

## 15. Limitations

- The initial version contains Python programming questions.
- Questions are maintained in a JSON file.
- The application runs locally using Flask.
- A persistent leaderboard is not included unless implemented as an additional feature.
- Internet access is not required during normal local quiz usage once dependencies are installed.

## 16. GitHub Repository

**Repository:** https://github.com/Sreevalli20/skill4.git

**Project:** Quiz and Assessment App

**Academic Module:** Python Programming – Week 4

## 17. Author

**Sreevalli**

Python Programming – Week 4 Project

---

Developed using Python 3.14.6, Flask, HTML, CSS, JavaScript, and JSON.
