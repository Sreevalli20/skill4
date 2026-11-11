/* Quiz & Assessment App - frontend logic */

"use strict";

const state = {
  questions: [],
  currentIndex: 0,
  answers: {}, // { questionId: selectedOption }
  submitting: false,
};

const els = {
  startScreen: document.getElementById("start-screen"),
  quizScreen: document.getElementById("quiz-screen"),
  resultScreen: document.getElementById("result-screen"),
  reviewScreen: document.getElementById("review-screen"),
  totalQuestions: document.getElementById("total-questions"),
  startBtn: document.getElementById("start-btn"),
  loadError: document.getElementById("load-error"),
  questionCounter: document.getElementById("question-counter"),
  answeredCount: document.getElementById("answered-count"),
  progressFill: document.getElementById("progress-fill"),
  questionText: document.getElementById("question-text"),
  optionsContainer: document.getElementById("options-container"),
  prevBtn: document.getElementById("prev-btn"),
  nextBtn: document.getElementById("next-btn"),
  submitBtn: document.getElementById("submit-btn"),
  quizError: document.getElementById("quiz-error"),
  scoreValue: document.getElementById("score-value"),
  scorePercent: document.getElementById("score-percent"),
  feedbackText: document.getElementById("feedback-text"),
  statCorrect: document.getElementById("stat-correct"),
  statIncorrect: document.getElementById("stat-incorrect"),
  statUnanswered: document.getElementById("stat-unanswered"),
  reviewBtn: document.getElementById("review-btn"),
  retryBtn: document.getElementById("retry-btn"),
  reviewList: document.getElementById("review-list"),
  reviewRetryBtn: document.getElementById("review-retry-btn"),
};

/* ---------- Screen helpers ---------- */

function showScreen(name) {
  for (const key of ["startScreen", "quizScreen", "resultScreen", "reviewScreen"]) {
    els[key].classList.toggle("active", key === name);
  }
}

function showError(el, message) {
  el.textContent = message;
  el.classList.remove("hidden");
}

function clearError(el) {
  el.textContent = "";
  el.classList.add("hidden");
}

/* ---------- Data loading ---------- */

async function loadQuestions() {
  try {
    const res = await fetch("/api/questions");
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || "Failed to load questions.");
    }
    state.questions = data.questions;
    els.totalQuestions.textContent = data.questions.length;
    return true;
  } catch (err) {
    showError(
      els.loadError,
      "Could not load the quiz. " + (err.message || "Please try again later.")
    );
    return false;
  }
}

/* ---------- Quiz rendering ---------- */

function renderQuestion() {
  const q = state.questions[state.currentIndex];
  const answered = Object.keys(state.answers).length;

  els.questionCounter.textContent =
    `Question ${state.currentIndex + 1} of ${state.questions.length}`;
  els.answeredCount.textContent = `${answered} answered`;
  els.progressFill.style.width =
    `${(answered / state.questions.length) * 100}%`;

  els.questionText.textContent = q.question;
  els.prevBtn.disabled = state.currentIndex === 0;
  els.nextBtn.textContent =
    state.currentIndex === state.questions.length - 1 ? "Last Question" : "Next";

  els.optionsContainer.innerHTML = "";
  q.options.forEach((option) => {
    const label = document.createElement("label");
    label.className = "option" + (state.answers[q.id] === option ? " selected" : "");

    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "answer";
    radio.value = option;
    radio.checked = state.answers[q.id] === option;
    radio.addEventListener("change", () => selectAnswer(q.id, option, label));

    const text = document.createElement("span");
    text.textContent = option;

    label.appendChild(radio);
    label.appendChild(text);
    els.optionsContainer.appendChild(label);
  });
}

function selectAnswer(qid, option, labelEl) {
  state.answers[qid] = option;
  document
    .querySelectorAll("#options-container .option")
    .forEach((el) => el.classList.remove("selected"));
  labelEl.classList.add("selected");
  clearError(els.quizError);
  els.answeredCount.textContent =
    `${Object.keys(state.answers).length} answered`;
  els.progressFill.style.width =
    `${(Object.keys(state.answers).length / state.questions.length) * 100}%`;
}

/* ---------- Navigation ---------- */

els.prevBtn.addEventListener("click", () => {
  if (state.currentIndex > 0) {
    state.currentIndex--;
    renderQuestion();
  }
});

els.nextBtn.addEventListener("click", () => {
  if (state.currentIndex < state.questions.length - 1) {
    state.currentIndex++;
    renderQuestion();
  }
});

/* ---------- Submission ---------- */

els.submitBtn.addEventListener("click", async () => {
  if (state.submitting) return;

  // Warn about unanswered questions.
  const unanswered = state.questions.filter((q) => !(q.id in state.answers));
  if (unanswered.length > 0) {
    const goBack = confirm(
      `${unanswered.length} question(s) are unanswered. ` +
      `Submit anyway? You can go back and answer them first.`
    );
    if (!goBack) {
      // Jump to the first unanswered question so the user can answer it.
      const firstUnanswered = state.questions.findIndex(
        (q) => !(q.id in state.answers)
      );
      if (firstUnanswered !== -1) {
        state.currentIndex = firstUnanswered;
        renderQuestion();
      }
      return;
    }
  }

  state.submitting = true;
  els.submitBtn.disabled = true;
  els.submitBtn.textContent = "Submitting...";
  clearError(els.quizError);

  try {
    const res = await fetch("/api/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answers: state.answers }),
    });
    const data = await res.json();

    if (!res.ok) {
      showError(els.quizError, data.error || "Submission failed. Please try again.");
      state.submitting = false;
      els.submitBtn.disabled = false;
      els.submitBtn.textContent = "Submit Quiz";
      return;
    }

    renderResults(data);
    showScreen("resultScreen");
  } catch (err) {
    showError(els.quizError, "Network error. Please check your connection and try again.");
  } finally {
    state.submitting = false;
    els.submitBtn.disabled = false;
    els.submitBtn.textContent = "Submit Quiz";
  }
});

/* ---------- Results & review ---------- */

function renderResults(data) {
  state.lastResults = data;
  els.scoreValue.textContent = data.score;
  els.scorePercent.textContent = `${data.percentage}%`;
  els.feedbackText.textContent = data.feedback;
  els.statCorrect.textContent = data.correct_answers;
  els.statIncorrect.textContent = data.incorrect_answers;
  els.statUnanswered.textContent = data.unanswered;
}

els.reviewBtn.addEventListener("click", () => {
  renderReview(state.lastResults);
  showScreen("reviewScreen");
});

els.retryBtn.addEventListener("click", resetQuiz);
els.reviewRetryBtn.addEventListener("click", resetQuiz);

function renderReview(results) {
  els.reviewList.innerHTML = "";
  results.review.forEach((item, idx) => {
    const div = document.createElement("div");
    let statusClass = "unanswered";
    let statusText = "Unanswered";
    if (item.is_correct) {
      statusClass = "correct";
      statusText = "Correct";
    } else if (item.selected !== null) {
      statusClass = "incorrect";
      statusText = "Incorrect";
    }
    div.className = `review-item ${statusClass}`;

    const selectedText = item.selected === null ? "— (not answered)" : item.selected;

    div.innerHTML = `
      <div class="review-status">Question ${idx + 1} — ${statusText}</div>
      <div class="review-question"></div>
      <div class="review-row"><strong>Your answer:</strong> <span class="review-selected"></span></div>
      <div class="review-row"><strong>Correct answer:</strong> <span class="review-correct"></span></div>
      <div class="review-explanation"></div>
    `;
    div.querySelector(".review-question").textContent = item.question;
    div.querySelector(".review-selected").textContent = selectedText;
    div.querySelector(".review-correct").textContent = item.correct_answer;
    div.querySelector(".review-explanation").textContent = `Explanation: ${item.explanation}`;
    els.reviewList.appendChild(div);
  });
}

/* ---------- Start & reset ---------- */

function resetQuiz() {
  state.currentIndex = 0;
  state.answers = {};
  state.submitting = false;
  clearError(els.quizError);
  renderQuestion();
  showScreen("quizScreen");
}

els.startBtn.addEventListener("click", async () => {
  if (state.questions.length === 0) {
    const ok = await loadQuestions();
    if (!ok) return;
  }
  resetQuiz();
});

// Initial load so the start screen shows the question count.
loadQuestions();
