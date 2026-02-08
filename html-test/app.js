// QuizMaster Pro - JavaScript Application
const API_BASE = 'https://backend-quiz-0ab2.onrender.com';

// État global de l'application
let currentUser = null;
let currentAttempt = null;
let currentQuiz = null;
let currentQuestionIndex = 0;
let quizQuestions = [];
let userAnswers = [];

// Utilitaires
function log(message, type = 'info') {
    const logsContainer = document.getElementById('logs-container');
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry ${type}`;
    logEntry.textContent = `[${timestamp}] ${message}`;
    logsContainer.appendChild(logEntry);
    logsContainer.scrollTop = logsContainer.scrollHeight;
}

function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    const section = document.getElementById(sectionId);
    if (section) section.classList.add('active');
    const btn = document.getElementById(`${sectionId.replace('-section', '')}-section-btn`);
    if (btn) btn.classList.add('active');
}

function updateAuthStatus() {
    const userInfo = document.getElementById('user-info');
    const logoutBtn = document.getElementById('logout-btn');
    const adminBtn = document.getElementById('admin-section-btn');
    
    if (currentUser) {
        userInfo.textContent = `${currentUser.name} (${currentUser.role})`;
        logoutBtn.style.display = 'inline-block';
        adminBtn.style.display = currentUser.role === 'admin' ? 'inline-block' : 'none';
    } else {
        userInfo.textContent = 'Non connecté';
        logoutBtn.style.display = 'none';
        adminBtn.style.display = 'none';
    }
}

// API Calls
async function apiCall(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const defaultOptions = {
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' }
    };
    
    try {
        log(`➡️ ${options.method || 'GET'} ${endpoint}`);
        const response = await fetch(url, { ...defaultOptions, ...options });
        log(`⬅️ ${response.status} ${response.statusText}`);
        
        if (response.ok) {
            const data = await response.json();
            log(`✅ Réponse reçue`, 'success');
            return data;
        } else {
            const error = await response.text();
            log(`❌ Erreur: ${error}`, 'error');
            throw new Error(`HTTP ${response.status}: ${error}`);
        }
    } catch (error) {
        log(`💥 Exception: ${error.message}`, 'error');
        throw error;
    }
}

// Authentification
async function register(name, email, password) {
    return await apiCall('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ name, email, password })
    });
}

async function login(email, password) {
    const result = await apiCall('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
    });
    const userInfo = await apiCall('/auth/me');
    currentUser = userInfo;
    updateAuthStatus();
    return result;
}

async function logout() {
    try {
        await apiCall('/auth/logout', { method: 'POST' });
        currentUser = null;
        updateAuthStatus();
        log('✅ Déconnexion réussie', 'success');
    } catch (error) {
        log('⚠️ Erreur déconnexion', 'error');
    }
}

// Catégories
async function loadCategories() {
    try {
        const result = await apiCall('/categories');
        displayCategories(result);
    } catch (error) {
        document.getElementById('categories-list').innerHTML = 
            `<p style="color: #fc8181;">❌ Erreur: ${error.message}</p>`;
    }
}

function displayCategories(categories) {
    const container = document.getElementById('categories-list');
    container.innerHTML = '';
    
    categories.forEach((category, index) => {
        const card = document.createElement('div');
        card.className = 'category-card';
        card.style.animationDelay = `${index * 0.1}s`;
        card.innerHTML = `
            <h4 style="font-size: 20px; margin-bottom: 10px; color: #2d3748;">${category.name}</h4>
            <p style="color: #718096; margin-bottom: 10px;">${category.description || 'Aucune description'}</p>
            <small style="color: #a0aec0;">ID: ${category.id}</small>
        `;
        card.onclick = () => selectCategory(category);
        container.appendChild(card);
    });
}

function selectCategory(category) {
    document.getElementById('category-title').textContent = category.name;
    document.getElementById('category-detail').style.display = 'block';
    document.getElementById('category-detail').dataset.categoryId = category.id;
}

async function loadCategoryQuizzes() {
    const categoryId = document.getElementById('category-detail').dataset.categoryId;
    if (!categoryId) return;
    
    try {
        const result = await apiCall(`/categories/${categoryId}/quizzes/available`);
        displayCategoryQuizzes(result.data);
    } catch (error) {
        document.getElementById('category-quizzes-list').innerHTML = 
            `<p style="color: #fc8181;">❌ Erreur: ${error.message}</p>`;
    }
}

function displayCategoryQuizzes(quizzes) {
    const container = document.getElementById('category-quizzes-list');
    container.innerHTML = '';
    
    quizzes.forEach((quiz, index) => {
        const card = document.createElement('div');
        card.className = `quiz-card ${quiz.is_accessible ? '' : 'locked'}`;
        card.style.animationDelay = `${index * 0.1}s`;
        card.innerHTML = `
            <h4 style="font-size: 18px; margin-bottom: 8px; color: #2d3748;">${quiz.title}</h4>
            <p style="color: #718096; margin-bottom: 8px;">Niveau: ${quiz.level}</p>
            <small style="color: #a0aec0;">ID: ${quiz.id}</small>
            ${quiz.is_accessible ? 
                '<div style="margin-top: 10px;"><span style="color: #48bb78; font-weight: 600;">✅ Accessible</span></div>' : 
                '<div style="margin-top: 10px;"><span style="color: #fc8181; font-weight: 600;">🔒 Verrouillé</span></div>'}
        `;
        
        if (quiz.is_accessible) {
            card.onclick = () => startQuiz(quiz);
        }
        
        container.appendChild(card);
    });
}

// Quiz - Démarrage
async function startQuiz(quiz) {
    try {
        const result = await apiCall(`/attempts/start/${quiz.id}`, { method: 'POST' });
        currentQuiz = result.quiz;
        currentAttempt = { id: result.attempt_id };
        quizQuestions = result.questions;
        userAnswers = [];
        currentQuestionIndex = 0;
        
        showSection('quiz-section');
        document.getElementById('quiz-info').style.display = 'none';
        document.getElementById('quiz-progress').style.display = 'block';
        document.getElementById('quiz-results').style.display = 'none';
        
        displayCurrentQuestion();
        log('✅ Quiz démarré', 'success');
        // show save button
        document.getElementById('save-progress-btn').style.display = 'inline-block';
        document.getElementById('resume-last-btn').style.display = 'none';
    } catch (error) {
        alert(`❌ Erreur lors du démarrage du quiz: ${error.message}`);
    }
}

// Quiz - Affichage question par question
function displayCurrentQuestion() {
    const questionsContainer = document.getElementById('quiz-questions');
    questionsContainer.innerHTML = '';
    questionsContainer.style.display = 'block';
    
    const question = quizQuestions[currentQuestionIndex];
    const totalQuestions = quizQuestions.length;
    
    // Mise à jour de la barre de progression
    const progress = ((currentQuestionIndex + 1) / totalQuestions) * 100;
    document.getElementById('progress-bar').style.width = `${progress}%`;
    document.getElementById('progress-text').textContent = 
        `Question ${currentQuestionIndex + 1} sur ${totalQuestions}`;
    
    const questionCard = document.createElement('div');
    questionCard.className = 'question-card';
    questionCard.innerHTML = `
        <div class="question-number">Question ${currentQuestionIndex + 1}/${totalQuestions}</div>
        <div class="question-text">${question.question_text}</div>
        <div class="answers" id="answers-container">
            ${question.answers.map((answer, index) => `
                <label class="answer-option" data-answer-id="${answer.id}">
                    <input type="checkbox" value="${answer.id}">
                    <span>${answer.answer_text}</span>
                </label>
            `).join('')}
        </div>
        <button id="validate-answer-btn" style="margin-top: 30px;">
            ${currentQuestionIndex < totalQuestions - 1 ? 
                'Valider et continuer ➡️' : 
                'Terminer le quiz 🎯'}
        </button>
    `;
    
    questionsContainer.appendChild(questionCard);
    
    // Gestion de la sélection des réponses
    document.querySelectorAll('.answer-option').forEach(option => {
        option.addEventListener('click', function(e) {
            if (e.target.tagName !== 'INPUT') {
                const checkbox = this.querySelector('input[type="checkbox"]');
                checkbox.checked = !checkbox.checked;
            }
            
            if (this.querySelector('input[type="checkbox"]').checked) {
                this.classList.add('selected');
            } else {
                this.classList.remove('selected');
            }
        });
    });
    
    document.getElementById('validate-answer-btn').onclick = validateCurrentAnswer;
}

// Save progress (partial answers)
async function saveProgress() {
    if (!currentAttempt || !currentAttempt.id) {
        alert('Aucune tentative active à sauvegarder');
        return;
    }

    // include current selected answers even if not validated
    const currentQuestion = quizQuestions[currentQuestionIndex];
    const currentSelected = Array.from(document.querySelectorAll('#answers-container input:checked')).map(i => i.value);

    // Build payload from userAnswers + currentSelected for current question
    const answersMap = {};
    userAnswers.forEach(a => { answersMap[a.question_id] = a.answer_ids; });
    if (currentSelected.length > 0) {
        answersMap[currentQuestion.id] = currentSelected;
    }

    const payload = { answers: Object.keys(answersMap).map(qid => ({ question_id: qid, answer_ids: answersMap[qid] })) };

    try {
        await apiCall(`/attempts/save/${currentAttempt.id}`, {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        alert('✅ Progression sauvegardée');
    } catch (err) {
        alert(`❌ Erreur sauvegarde: ${err.message}`);
    }
}

// Resume a specific quiz attempt by quiz id
async function resumeAttemptByQuizId(quizId) {
    try {
        const result = await apiCall(`/attempts/resume/${quizId}`);
        // result contains attempt_id, quiz, questions (with user_selected flags)
        currentAttempt = { id: result.attempt_id };
        currentQuiz = result.quiz;
        quizQuestions = result.questions;
        // build userAnswers from questions which have user_selected
        userAnswers = [];
        quizQuestions.forEach(q => {
            const selected = q.answers.filter(a => a.user_selected).map(a => a.id);
            if (selected.length) userAnswers.push({ question_id: q.id, answer_ids: selected });
        });

        // find first unanswered question index
        const firstUnanswered = quizQuestions.findIndex(q => !q.answers.some(a => a.user_selected));
        currentQuestionIndex = firstUnanswered === -1 ? 0 : firstUnanswered;

        showSection('quiz-section');
        document.getElementById('quiz-info').style.display = 'none';
        document.getElementById('quiz-progress').style.display = 'block';
        document.getElementById('quiz-results').style.display = 'none';
        document.getElementById('save-progress-btn').style.display = 'inline-block';
        displayCurrentQuestion();
        log('↩️ Tentative reprise', 'success');
    } catch (err) {
        alert(`❌ Erreur reprise: ${err.message}`);
    }
}

// List in-progress attempts
async function loadInProgressAttempts() {
    try {
        const result = await apiCall('/attempts/in-progress');
        displayInProgressAttempts(result.data);
    } catch (err) {
        document.getElementById('attempts-list').innerHTML = `<p style="color: #fc8181;">❌ Erreur: ${err.message}</p>`;
    }
}

function displayInProgressAttempts(attempts) {
    const container = document.getElementById('attempts-list');
    container.innerHTML = '';
    if (!attempts || attempts.length === 0) {
        container.innerHTML = '<p style="text-align:center; color:#718096; padding:40px;">Aucune tentative en cours</p>';
        return;
    }

    attempts.forEach((attempt, index) => {
        const card = document.createElement('div');
        card.className = 'attempt-card';
        card.style.animationDelay = `${index * 0.1}s`;
        card.innerHTML = `
            <h4 style="font-size:18px; margin-bottom:10px; color:#2d3748;">${attempt.quiz_title || attempt.quiz_id}</h4>
            <p style="color:#718096; margin-bottom:8px;">Tentative en cours</p>
            <small style="color:#a0aec0;">Attempt ID: ${attempt.attempt_id}</small>
            <div style="margin-top:10px;"></div>
        `;
        const btn = document.createElement('button');
        btn.textContent = '↩️ Reprendre';
        btn.onclick = () => resumeAttemptByQuizId(attempt.quiz_id);
        card.appendChild(btn);
        container.appendChild(card);
    });
}

// Quiz - Validation de la réponse actuelle
function validateCurrentAnswer() {
    const question = quizQuestions[currentQuestionIndex];
    const selectedAnswers = Array.from(
        document.querySelectorAll('#answers-container input:checked')
    ).map(input => input.value);
    
    if (selectedAnswers.length === 0) {
        alert('⚠️ Veuillez sélectionner au moins une réponse');
        return;
    }
    
    userAnswers.push({
        question_id: question.id,
        answer_ids: selectedAnswers
    });
    
    if (currentQuestionIndex < quizQuestions.length - 1) {
        currentQuestionIndex++;
        displayCurrentQuestion();
    } else {
        submitQuiz();
    }
}

// Quiz - Soumission finale
async function submitQuiz() {
    try {
        const result = await apiCall(`/attempts/submit/${currentAttempt.id}`, {
            method: 'POST',
            body: JSON.stringify({ answers: userAnswers })
        });
        
        displayQuizResults(result);
        log('✅ Quiz soumis', 'success');
    } catch (error) {
        alert(`❌ Erreur lors de la soumission: ${error.message}`);
    }
}

// Quiz - Affichage des résultats
function displayQuizResults(results) {
    document.getElementById('quiz-questions').style.display = 'none';
    document.getElementById('quiz-progress').style.display = 'none';
    
    const resultsContainer = document.getElementById('quiz-results');
    resultsContainer.innerHTML = `
        <div style="text-align: center; margin-bottom: 40px;">
            <h3 style="font-size: 32px; margin-bottom: 20px;">
                ${results.passed ? '🎉 Félicitations !' : '📚 Continuez vos efforts !'}
            </h3>
            <p style="font-size: 18px; color: #718096;">Voici vos résultats</p>
        </div>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">${results.score}%</div>
                <div class="stat-label">Score</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${results.passed ? '✅' : '❌'}</div>
                <div class="stat-label">${results.passed ? 'Réussi' : 'Échoué'}</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${results.correct_answers}/${results.total_questions}</div>
                <div class="stat-label">Questions correctes</div>
            </div>
        </div>
        <div style="display: flex; gap: 15px; margin-top: 30px;">
            <button onclick="showSection('attempts-section'); loadUserAttempts();" style="flex: 1;">
                📊 Voir mes tentatives
            </button>
            <button onclick="showSection('categories-section');" style="flex: 1;">
                📚 Retour aux catégories
            </button>
        </div>
    `;
    
    resultsContainer.style.display = 'block';
}

// Tentatives
async function loadUserAttempts() {
    try {
        const result = await apiCall('/users/me/attempts');
        displayAttempts(result);
    } catch (error) {
        document.getElementById('attempts-list').innerHTML = 
            `<p style="color: #fc8181;">❌ Erreur: ${error.message}</p>`;
    }
}

function displayAttempts(attempts) {
    const container = document.getElementById('attempts-list');
    container.innerHTML = '';
    
    if (attempts.length === 0) {
        container.innerHTML = 
            '<p style="text-align: center; color: #718096; padding: 40px;">Aucune tentative pour le moment</p>';
        return;
    }
    
    attempts.forEach((attempt, index) => {
        const card = document.createElement('div');
        card.className = 'attempt-card';
        card.style.animationDelay = `${index * 0.1}s`;
        card.innerHTML = `
            <h4 style="font-size: 18px; margin-bottom: 10px; color: #2d3748;">${attempt.quiz_title}</h4>
            <p style="color: #718096; margin-bottom: 5px;">
                Score: <strong style="color: ${attempt.passed ? '#48bb78' : '#fc8181'};">${attempt.score}%</strong>
            </p>
            <p style="color: #718096; margin-bottom: 10px;">
                Résultat: ${attempt.passed ? 
                    '<span style="color: #48bb78; font-weight: 600;">✅ Réussi</span>' : 
                    '<span style="color: #fc8181; font-weight: 600;">❌ Échoué</span>'}
            </p>
            <small style="color: #a0aec0;">${new Date(attempt.completed_at).toLocaleString('fr-FR')}</small>
        `;
        card.onclick = () => loadAttemptDetail(attempt.id);
        container.appendChild(card);
    });
}

async function loadAttemptDetail(attemptId) {
    try {
        const result = await apiCall(`/attempts/${attemptId}`);
        displayAttemptDetail(result.data);
        document.getElementById('attempt-detail').style.display = 'block';
    } catch (error) {
        alert(`❌ Erreur: ${error.message}`);
    }
}

function displayAttemptDetail(data) {
    const container = document.getElementById('attempt-results');
    container.innerHTML = `
        <h4 style="font-size: 24px; margin-bottom: 15px;">${data.quiz.title}</h4>
        <p style="font-size: 18px; margin-bottom: 30px;">
            Score: <strong style="color: ${data.attempt.passed ? '#48bb78' : '#fc8181'};">
                ${data.attempt.score}%
            </strong> - ${data.attempt.passed ? '✅ Réussi' : '❌ Échoué'}
        </p>
        <h5 style="margin-bottom: 20px; color: #4a5568;">Questions du quiz:</h5>
        <div class="info-card" style="margin-bottom: 20px;">
            <p style="color: #2c5282;">
                💡 Les détails des réponses utilisateur ne sont pas disponibles pour les tentatives passées.
            </p>
        </div>
    `;
    
    data.questions_with_answers.forEach((question, index) => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question-card';
        questionDiv.style.animationDelay = `${index * 0.1}s`;
        questionDiv.innerHTML = `
            <div class="question-number">Question ${index + 1}</div>
            <p style="font-size: 16px; font-weight: 600; margin-bottom: 15px;">${question.question_text}</p>
            <p style="color: #48bb78; font-weight: 500;">
                ✅ Réponses correctes: ${question.answers.filter(a => a.is_correct).map(a => a.answer_text).join(', ')}
            </p>
        `;
        container.appendChild(questionDiv);
    });
}

// Admin
async function loadAdminStats() {
    try {
        const result = await apiCall('/admin/stats');
        displayAdminStats(result);
    } catch (error) {
        document.getElementById('admin-stats').innerHTML = 
            `<p style="color: #fc8181;">❌ Erreur: ${error.message}</p>`;
    }
}

function displayAdminStats(stats) {
    const container = document.getElementById('admin-stats');
    container.innerHTML = `
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">${stats.total_users}</div>
                <div class="stat-label">👥 Utilisateurs</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${stats.total_quizzes}</div>
                <div class="stat-label">🎯 Quiz</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${stats.total_categories}</div>
                <div class="stat-label">📚 Catégories</div>
            </div>
        </div>
    `;
}

async function loadUsers() {
    try {
        const result = await apiCall('/admin/users');
        displayUsers(result.data);
    } catch (error) {
        document.getElementById('users-list').innerHTML = 
            `<p style="color: #fc8181;">❌ Erreur: ${error.message}</p>`;
    }
}

function displayUsers(users) {
    const container = document.getElementById('users-list');
    container.innerHTML = '';
    
    users.forEach((user, index) => {
        const card = document.createElement('div');
        card.className = 'user-card';
        card.style.animationDelay = `${index * 0.1}s`;
        card.innerHTML = `
            <h4 style="font-size: 18px; margin-bottom: 8px; color: #2d3748;">${user.name}</h4>
            <p style="color: #718096; margin-bottom: 5px;">${user.email}</p>
            <p style="color: #718096; margin-bottom: 8px;">
                Rôle: <strong>${user.role === 'admin' ? '👑 Admin' : '👤 Utilisateur'}</strong>
            </p>
            <small style="color: #a0aec0;">ID: ${user.id}</small>
        `;
        container.appendChild(card);
    });
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Navigation
    document.getElementById('auth-section-btn').onclick = () => showSection('auth-section');
    document.getElementById('categories-section-btn').onclick = () => showSection('categories-section');
    document.getElementById('quiz-section-btn').onclick = () => showSection('quiz-section');
    document.getElementById('attempts-section-btn').onclick = () => showSection('attempts-section');
    document.getElementById('admin-section-btn').onclick = () => showSection('admin-section');
    
    // Authentification
    document.getElementById('register-btn').onclick = async () => {
        const name = document.getElementById('register-name').value;
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;
        
        try {
            await register(name, email, password);
            document.getElementById('auth-result').innerHTML = `
                <div class="info-card">
                    <p style="color: #48bb78; font-weight: 600;">
                        ✅ Inscription réussie ! Vous pouvez maintenant vous connecter.
                    </p>
                </div>
            `;
        } catch (error) {
            document.getElementById('auth-result').innerHTML = `
                <div class="info-card" style="background: #fed7d7; border-left-color: #fc8181;">
                    <p style="color: #c53030; font-weight: 600;">❌ Erreur: ${error.message}</p>
                </div>
            `;
        }
    };
    
    document.getElementById('login-btn').onclick = async () => {
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        
        try {
            await login(email, password);
            document.getElementById('auth-result').innerHTML = `
                <div class="info-card">
                    <p style="color: #48bb78; font-weight: 600;">✅ Connexion réussie !</p>
                </div>
            `;
            setTimeout(() => {
                showSection('categories-section');
                loadCategories();
            }, 1000);
        } catch (error) {
            document.getElementById('auth-result').innerHTML = `
                <div class="info-card" style="background: #fed7d7; border-left-color: #fc8181;">
                    <p style="color: #c53030; font-weight: 600;">❌ Erreur: ${error.message}</p>
                </div>
            `;
        }
    };
    
    document.getElementById('logout-btn').onclick = logout;
    
    // Catégories
    document.getElementById('load-categories-btn').onclick = loadCategories;
    document.getElementById('load-category-quizzes-btn').onclick = loadCategoryQuizzes;
    
    // Quiz
    document.getElementById('go-to-categories-btn').onclick = () => {
        showSection('categories-section');
        loadCategories();
    };
    
    // Tentatives
    document.getElementById('load-attempts-btn').onclick = loadUserAttempts;
    document.getElementById('load-inprogress-btn').onclick = loadInProgressAttempts;

    document.getElementById('save-progress-btn').onclick = saveProgress;
    document.getElementById('resume-last-btn').onclick = async () => {
        // try to resume last in-progress attempt for current quiz (if any)
        if (!currentQuiz) {
            alert('Aucun quiz sélectionné');
            return;
        }
        await resumeAttemptByQuizId(currentQuiz.id);
    };
    
    // Admin
    document.getElementById('load-admin-stats-btn').onclick = loadAdminStats;
    document.getElementById('load-users-btn').onclick = loadUsers;
    
    // Logs
    document.getElementById('clear-logs-btn').onclick = () => {
        document.getElementById('logs-container').innerHTML = '';
    };
    
    // Initialisation
    updateAuthStatus();
    log('🚀 QuizMaster Pro - Application démarrée avec succès', 'success');
});