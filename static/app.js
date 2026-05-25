const STORAGE_KEYS = {
  users: 'qwss_users',
  scores: 'qwss_scores',
  session: 'qwss_session',
  quiz: 'qwss_quiz_state'
};

const QUESTIONS = [
  { id: 1, category: 'Monumentos', question: '¿Qué monumento de Sevilla fue construido para la Exposición Iberoamericana de 1929?', options: ['La Giralda', 'La Plaza de España', 'La Torre del Oro', 'El Alcázar'], answer: 'B' },
  { id: 2, category: 'Historia', question: '¿En qué siglo comenzó la construcción de la Catedral de Sevilla?', options: ['Siglo XII', 'Siglo XIII', 'Siglo XV', 'Siglo XVIII'], answer: 'C' },
  { id: 3, category: 'Geografía', question: '¿Qué río atraviesa Sevilla?', options: ['Guadalquivir', 'Tajo', 'Ebro', 'Duero'], answer: 'A' },
  { id: 4, category: 'Cultura', question: '¿Qué fiesta es una de las más conocidas de Sevilla?', options: ['La Tomatina', 'La Feria de Abril', 'Las Fallas', 'Los Sanfermines'], answer: 'B' },
  { id: 5, category: 'Tradiciones', question: '¿Qué procesión tiene gran importancia en la Semana Santa sevillana?', options: ['La Madrugá', 'El Rocío', 'La Mercè', 'San Isidro'], answer: 'A' },
  { id: 6, category: 'Monumentos', question: '¿Cómo se llama la famosa torre almohade junto al río?', options: ['Torre del Oro', 'Torre de Pisa', 'Torre Blanca', 'Torre Sevilla'], answer: 'A' },
  { id: 7, category: 'Historia', question: '¿Qué civilización dejó una fuerte huella en Sevilla?', options: ['Vikingos', 'Romanos y musulmanes', 'Mayas', 'Incas'], answer: 'B' },
  { id: 8, category: 'Cultura', question: '¿Cuál es una bebida típica asociada a Sevilla y a Andalucía?', options: ['Horchata', 'Rebujito', 'Sake', 'Kombucha'], answer: 'B' },
  { id: 9, category: 'Tradiciones', question: '¿En qué mes suele celebrarse la Feria de Abril?', options: ['Abril', 'Junio', 'Septiembre', 'Diciembre'], answer: 'A' },
  { id: 10, category: 'Monumentos', question: '¿Qué palacio es famoso por su arquitectura mudéjar?', options: ['Alcázar de Sevilla', 'Palacio Real de Madrid', 'La Alhambra de Granada', 'Casa Batlló'], answer: 'A' }
];

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));

const state = {
  session: loadJSON(STORAGE_KEYS.session, null),
  users: loadJSON(STORAGE_KEYS.users, []),
  scores: loadJSON(STORAGE_KEYS.scores, []),
  quiz: loadJSON(STORAGE_KEYS.quiz, null)
};

function loadJSON(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

function saveJSON(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

function uid(prefix) {
  return `${prefix}_${Math.random().toString(36).slice(2, 10)}_${Date.now()}`;
}

function setNotice(containerId, message, type = 'error') {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = message ? `<div class="notice ${type}">${message}</div>` : '';
}

function showOnly(sectionId) {
  ['authSection', 'dashboardSection', 'quizSection', 'resultSection'].forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.classList.toggle('hidden', id !== sectionId);
  });
}

function persist() {
  saveJSON(STORAGE_KEYS.users, state.users);
  saveJSON(STORAGE_KEYS.scores, state.scores);
  saveJSON(STORAGE_KEYS.session, state.session);
  saveJSON(STORAGE_KEYS.quiz, state.quiz);
}

function getCurrentUser() {
  return state.session ? state.users.find((u) => u.id === state.session.userId) || null : null;
}

function requireSession() {
  if (!state.session) {
    showOnly('authSection');
    return false;
  }
  return true;
}

function registerUser(event) {
  event.preventDefault();
  const form = new FormData(event.target);
  const name = String(form.get('name') || '').trim();
  const email = String(form.get('email') || '').trim().toLowerCase();
  const password = String(form.get('password') || '');

  if (name.length < 3) return setNotice('authNotice', 'El nombre debe tener al menos 3 caracteres.');
  if (!email.includes('@')) return setNotice('authNotice', 'Introduce un email válido.');
  if (password.length < 6) return setNotice('authNotice', 'La contraseña debe tener al menos 6 caracteres.');
  if (state.users.some((u) => u.email === email)) return setNotice('authNotice', 'Ese email ya está registrado.');

  const user = { id: uid('usr'), name, email, password, createdAt: new Date().toISOString() };
  state.users.push(user);
  state.session = { userId: user.id };
  persist();
  event.target.reset();
  setNotice('authNotice', 'Registro completado. Ya has iniciado sesión.', 'success');
  renderAll();
  showOnly('dashboardSection');
}

function loginUser(event) {
  event.preventDefault();
  const form = new FormData(event.target);
  const email = String(form.get('email') || '').trim().toLowerCase();
  const password = String(form.get('password') || '');
  const user = state.users.find((u) => u.email === email && u.password === password);
  if (!user) return setNotice('authNotice', 'Email o contraseña incorrectos.');
  state.session = { userId: user.id };
  persist();
  event.target.reset();
  setNotice('authNotice', 'Sesión iniciada correctamente.', 'success');
  renderAll();
  showOnly('dashboardSection');
}

function logout() {
  state.session = null;
  state.quiz = null;
  persist();
  renderAll();
  showOnly('authSection');
}

function getUserScores(userId) {
  return state.scores.filter((score) => score.userId === userId).sort((a, b) => new Date(b.date) - new Date(a.date));
}

function getLeaderboard() {
  const grouped = new Map();
  state.scores.forEach((score) => {
    const current = grouped.get(score.userId) || { userId: score.userId, name: score.userName, attempts: 0, best: 0, total: 0 };
    current.attempts += 1;
    current.best = Math.max(current.best, score.percentage);
    current.total += score.percentage;
    grouped.set(score.userId, current);
  });
  return Array.from(grouped.values())
    .map((row) => ({ ...row, average: row.attempts ? row.total / row.attempts : 0 }))
    .sort((a, b) => b.best - a.best || b.average - a.average || b.attempts - a.attempts || a.name.localeCompare(b.name));
}

function renderLeaderboard() {
  const tbody = $('#leaderboardBody');
  if (!tbody) return;
  const leaderboard = getLeaderboard();
  if (!leaderboard.length) {
    tbody.innerHTML = '<tr><td colspan="5" class="muted">Aún no hay puntuaciones registradas.</td></tr>';
    return;
  }
  tbody.innerHTML = leaderboard.slice(0, 10).map((row, index) => `
    <tr>
      <td>${index + 1}</td>
      <td>${escapeHTML(row.name)}</td>
      <td>${row.attempts}</td>
      <td>${Math.round(row.best)}%</td>
      <td>${row.average.toFixed(1)}%</td>
    </tr>
  `).join('');
}

function renderRecentScores() {
  const root = $('#recentList');
  if (!root) return;
  const recent = [...state.scores].sort((a, b) => new Date(b.date) - new Date(a.date)).slice(0, 6);
  if (!recent.length) {
    root.innerHTML = '<div class="result-item"><strong>No hay resultados aún.</strong><div class="result-meta">La primera puntuación aparecerá aquí.</div></div>';
    return;
  }
  root.innerHTML = recent.map((score) => `
    <div class="result-item ${score.percentage >= 60 ? 'good' : 'bad'}">
      <strong>${escapeHTML(score.userName)} — ${score.percentage}%</strong>
      <div class="result-meta">${new Date(score.date).toLocaleString('es-ES')} · ${score.correct}/${score.total} correctas</div>
    </div>
  `).join('');
}

function renderDashboard() {
  const user = getCurrentUser();
  if (!user) return;
  const scores = getUserScores(user.id);
  $('#sessionInfo').textContent = `Hola, ${user.name}`;
  $('#welcomeTitle').textContent = `📊 Bienvenido, ${user.name}`;
  $('#welcomeSubtitle').textContent = user.email;
  $('#statAttempts').textContent = scores.length;
  $('#statBest').textContent = scores.length ? `${Math.max(...scores.map((s) => s.percentage)).toFixed(0)}%` : '0%';
  $('#statAvg').textContent = scores.length ? `${(scores.reduce((acc, s) => acc + s.percentage, 0) / scores.length).toFixed(1)}%` : '0%';
  const history = $('#personalHistory');
  if (history) {
    history.innerHTML = scores.length ? scores.map((score) => `
      <div class="result-item ${score.percentage >= 60 ? 'good' : 'bad'}">
        <strong>${score.percentage}%</strong>
        <div class="result-meta">${new Date(score.date).toLocaleString('es-ES')} · ${score.correct}/${score.total} correctas</div>
      </div>
    `).join('') : '<div class="result-item"><strong>Aún no has jugado.</strong><div class="result-meta">Pulsa “Comenzar quiz” para estrenar tu marcador.</div></div>';
  }
}

function startQuiz() {
  if (!requireSession()) return;
  state.quiz = {
    questions: shuffle([...QUESTIONS]).slice(0, 10),
    current: 0,
    answers: []
  };
  persist();
  renderQuiz();
  showOnly('quizSection');
}

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function renderQuiz() {
  if (!state.quiz) return;
  const q = state.quiz.questions[state.quiz.current];
  $('#quizTitle').textContent = `Pregunta ${state.quiz.current + 1} de ${state.quiz.questions.length}`;
  $('#quizCategory').textContent = `Categoría: ${q.category}`;
  $('#quizQuestion').textContent = q.question;
  $('#quizProgressBar').style.width = `${(state.quiz.current / state.quiz.questions.length) * 100}%`;
  $('#quizProgressText').textContent = `${Math.round((state.quiz.current / state.quiz.questions.length) * 100)}%`;
  $('#nextQuestionBtn').textContent = state.quiz.current === state.quiz.questions.length - 1 ? 'Finalizar quiz' : 'Siguiente';
  const options = $('#quizOptions');
  options.innerHTML = q.options.map((option, index) => {
    const value = ['A', 'B', 'C', 'D'][index];
    return `
      <label class="quiz-option">
        <input type="radio" name="answer" value="${value}" required>
        <div><strong>${value}.</strong> ${escapeHTML(option)}</div>
      </label>
    `;
  }).join('');
  setNotice('quizNotice', '');
}

function submitQuizAnswer(event) {
  event.preventDefault();
  if (!state.quiz) return;
  const selected = new FormData(event.target).get('answer');
  if (!selected) return setNotice('quizNotice', 'Selecciona una respuesta antes de continuar.');
  const q = state.quiz.questions[state.quiz.current];
  state.quiz.answers.push({ questionId: q.id, question: q.question, selected, correct: q.answer, category: q.category });
  state.quiz.current += 1;
  persist();
  if (state.quiz.current >= state.quiz.questions.length) {
    finishQuiz();
    return;
  }
  renderQuiz();
  event.target.reset();
}

function finishQuiz() {
  if (!state.quiz) return;
  const user = getCurrentUser();
  const correct = state.quiz.answers.filter((a) => a.selected === a.correct).length;
  const total = state.quiz.questions.length;
  const percentage = Math.round((correct / total) * 100);
  const score = {
    id: uid('score'),
    userId: user.id,
    userName: user.name,
    percentage,
    correct,
    total,
    date: new Date().toISOString(),
    answers: state.quiz.answers
  };
  state.scores.push(score);
  persist();
  renderResult(score);
  state.quiz = null;
  persist();
  showOnly('resultSection');
}

function renderResult(score) {
  $('#resultScore').textContent = `${score.percentage}%`;
  $('#resultSummary').textContent = `${score.correct} de ${score.total} respuestas correctas.`;
  $('#resultDetails').innerHTML = score.answers.map((a, idx) => `
    <div class="result-item ${a.selected === a.correct ? 'good' : 'bad'}">
      <strong>${idx + 1}. ${escapeHTML(a.question)}</strong>
      <div class="result-meta">Tu respuesta: ${a.selected} · Correcta: ${a.correct}</div>
    </div>
  `).join('');
  renderAll();
}

function cancelQuiz() {
  state.quiz = null;
  persist();
  showOnly(state.session ? 'dashboardSection' : 'authSection');
}

function escapeHTML(str) {
  return String(str)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function renderAll() {
  renderLeaderboard();
  renderRecentScores();
  if (state.session && getCurrentUser()) {
    renderDashboard();
    $('#navDashboardBtn').classList.remove('hidden');
    $('#navLogoutBtn').classList.remove('hidden');
    $('#sessionInfo').textContent = `Hola, ${getCurrentUser().name}`;
  } else {
    $('#sessionInfo').textContent = 'Sin sesión';
    $('#navDashboardBtn').classList.add('hidden');
    $('#navLogoutBtn').classList.add('hidden');
  }
}

function initTabs() {
  const loginView = $('#loginView');
  const registerView = $('#registerView');
  $$('.tab-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      $$('.tab-btn').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      const tab = btn.dataset.authTab;
      loginView.classList.toggle('hidden', tab !== 'login');
      registerView.classList.toggle('hidden', tab !== 'register');
    });
  });
}

function bindEvents() {
  $('#registerForm').addEventListener('submit', registerUser);
  $('#loginForm').addEventListener('submit', loginUser);
  $('#navLogoutBtn').addEventListener('click', logout);
  $('#logoutBtn2').addEventListener('click', logout);
  $('#startQuizBtn').addEventListener('click', startQuiz);
  $('#goPlayBtn').addEventListener('click', () => state.session ? showOnly('dashboardSection') : showOnly('authSection'));
  $('#goAuthBtn').addEventListener('click', () => showOnly('authSection'));
  $('#brandHome').addEventListener('click', (e) => { e.preventDefault(); showOnly('authSection'); });
  $('#navDashboardBtn').addEventListener('click', () => { if (requireSession()) showOnly('dashboardSection'); });
  $('#quizForm').addEventListener('submit', submitQuizAnswer);
  $('#cancelQuizBtn').addEventListener('click', cancelQuiz);
  $('#playAgainBtn').addEventListener('click', startQuiz);
  $('#backDashboardBtn').addEventListener('click', () => showOnly('dashboardSection'));
}

function boot() {
  initTabs();
  bindEvents();
  renderAll();
  if (state.session && getCurrentUser()) {
    showOnly('dashboardSection');
  } else {
    showOnly('authSection');
  }
}

document.addEventListener('DOMContentLoaded', boot);