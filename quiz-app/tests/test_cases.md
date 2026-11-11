# Manual Test Report — Quiz and Assessment App

Environment: Python 3.14.6, Flask 3.0.3, Windows.
App run with `python app.py` at http://127.0.0.1:5000.
Automated suite: 29 tests, all passing (`python -m unittest discover -s tests`).

Legend: **Pass** = verified by execution; **Pass (API)** = verified through the
backend API / automated tests; **Manual** = requires a browser click-through.

| ID | Test Case | Steps | Expected | Actual | Result |
|----|-----------|-------|----------|--------|--------|
| TC_QUIZ_01 | Answer all questions correctly | Start quiz, select correct option for all 10, submit | 10/10, 100%, "Excellent work!" | API returned score `10/10`, `percentage: 100.0`, feedback `Excellent work!`; `test_submit_all_correct` passes | Pass (API) |
| TC_QUIZ_02 | Answer all questions incorrectly | Select a wrong option for every question, submit | 0/10, 0%, "Keep practicing, you can do better!" | API returned `0/10`, `0.0%`, correct feedback; `test_submit_all_wrong` passes | Pass (API) |
| TC_QUIZ_03 | Submit with unanswered questions | Leave some questions unanswered and click Submit | Warning shown; user can go back and answer | Frontend shows a `confirm()` warning listing the unanswered count and jumps to the first unanswered question if the user cancels. Unanswered count is also reported by the API (`unanswered` field) and covered by `test_submit_unanswered` | Pass (API + code); visual check recommended |
| TC_QUIZ_04 | Missing questions file | Rename/remove `data/questions.json`, reload | Friendly error, no traceback | `load_questions` returns "Questions file not found: questions.json"; `/api/questions` responds HTTP 500 with `{"error": ...}` JSON; covered by `test_missing_file` | Pass (API) |
| TC_QUIZ_05 | Broken JSON | Corrupt `questions.json` syntax, reload | Friendly data-loading error | `load_questions` returns "Invalid JSON in questions file: ... (line N)"; covered by `test_malformed_json` | Pass (API) |
| TC_QUIZ_06 | Invalid answer | POST `{"answers": {"1": "bogus"}}` to `/api/submit` | Reject the invalid answer | HTTP 400 `{"error": "Invalid answer for question 1."}`; `test_invalid_answer_value` passes | Pass (API) |
| TC_QUIZ_07 | All questions answered | Submit a full set of answers | Exact score calculated | Verified: 5 correct + 1 wrong + 4 unanswered → `5/10`, `50.0%`, "Good job, keep improving!" (`test_partially_unanswered`); boundary feedback verified in `test_feedback_boundaries` | Pass (API) |
| TC_QUIZ_08 | Retry quiz | Click Retry Quiz on the result screen | Answers and results reset | `resetQuiz()` clears `state.answers`, resets index to 0, re-renders question 1 | Manual (code-verified) |
| TC_QUIZ_09 | Rapid repeated clicks | Double/triple-click Submit Quiz quickly | Only one submission processed | `state.submitting` flag + `submitBtn.disabled` prevent duplicate POSTs; backend is stateless so repeated valid POSTs return identical results (`test_repeated_submission_is_stateless`) | Pass (API) + Manual |
| TC_QUIZ_10 | Mobile responsiveness | Open app at ~375px width | Layout remains usable | Responsive CSS: single-column options, full-width nav buttons, scaled cards under 600px; viewport meta tag present | Manual (code-verified) |

## Notes

- Correct answers and explanations are never sent by `/api/questions`
  (verified by `test_questions_api_hides_answers` and a live check).
- All backend behaviors above were additionally verified against the live
  server with `curl`/Python `urllib` during development.
- Frontend-only interactions (TC_QUIZ_03 warning dialog, TC_QUIZ_08 retry,
  TC_QUIZ_09 click spam, TC_QUIZ_10 layout) are implemented in
  `frontend/script.js` / `frontend/style.css` and should be confirmed with a
  quick browser pass before submission.
