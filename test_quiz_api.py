"""
Script de test des endpoints Quiz avec sauvegarde/reprise

Usage:
    python test_quiz_api.py
"""

import requests
import json
import time
from typing import Optional, Dict, List

# Configuration
API_BASE = "https://backend-quiz-0ab2.onrender.com"
SESSION = requests.Session()

# Couleurs pour les logs
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def log(message: str, level: str = "info"):
    """Logs colorisés"""
    timestamp = time.strftime("%H:%M:%S")
    if level == "success":
        print(f"{Colors.OKGREEN}[{timestamp}] ✅ {message}{Colors.ENDC}")
    elif level == "error":
        print(f"{Colors.FAIL}[{timestamp}] ❌ {message}{Colors.ENDC}")
    elif level == "warning":
        print(f"{Colors.WARNING}[{timestamp}] ⚠️  {message}{Colors.ENDC}")
    elif level == "info":
        print(f"{Colors.OKCYAN}[{timestamp}] ℹ️  {message}{Colors.ENDC}")
    else:
        print(f"[{timestamp}] {message}")


def api_call(method: str, endpoint: str, data: Optional[Dict] = None, json_format: bool = True) -> Optional[Dict]:
    """Effectue un appel API"""
    url = f"{API_BASE}{endpoint}"
    
    try:
        log(f"➡️  {method} {endpoint}")
        
        if method.upper() == "GET":
            response = SESSION.get(url, headers={"Content-Type": "application/json"})
        elif method.upper() == "POST":
            response = SESSION.post(url, json=data, headers={"Content-Type": "application/json"})
        elif method.upper() == "PUT":
            response = SESSION.put(url, json=data, headers={"Content-Type": "application/json"})
        elif method.upper() == "DELETE":
            response = SESSION.delete(url, headers={"Content-Type": "application/json"})
        else:
            raise ValueError(f"Méthode HTTP non supportée: {method}")
        
        log(f"⬅️  {response.status_code} {response.reason}")
        
        if response.ok:
            if json_format:
                data = response.json()
                log(f"✅ Réponse reçue ({len(str(data))} chars)", "success")
                return data
            else:
                log("✅ Réponse reçue", "success")
                return response.text
        else:
            error_text = response.text[:200]
            log(f"❌ Erreur: {error_text}", "error")
            return None
            
    except Exception as e:
        log(f"💥 Exception: {str(e)}", "error")
        return None


def register_user(name: str, email: str, password: str) -> bool:
    """Inscription d'un nouvel utilisateur"""
    print(f"\n{Colors.BOLD}=== INSCRIPTION ==={Colors.ENDC}")
    result = api_call("POST", "/auth/register", {
        "name": name,
        "email": email,
        "password": password
    })
    return result is not None


def login_user(email: str, password: str) -> bool:
    """Connexion utilisateur"""
    print(f"\n{Colors.BOLD}=== CONNEXION ==={Colors.ENDC}")
    result = api_call("POST", "/auth/login", {
        "email": email,
        "password": password
    })
    if result and "access_token" in result:
        token = result["access_token"]
        SESSION.headers.update({"Authorization": f"Bearer {token}"})
        # Le cookie est aussi défini automatiquement par requests.Session
        log(f"Token reçu et stocké", "success")
        return True
    return False


def get_profile() -> Optional[Dict]:
    """Récupère le profil de l'utilisateur"""
    print(f"\n{Colors.BOLD}=== MON PROFIL ==={Colors.ENDC}")
    return api_call("GET", "/auth/me")


def get_categories() -> Optional[List[Dict]]:
    """Récupère les catégories"""
    print(f"\n{Colors.BOLD}=== CATÉGORIES ==={Colors.ENDC}")
    result = api_call("GET", "/categories")
    if result and isinstance(result, list):
        log(f"📚 {len(result)} catégories trouvées", "success")
        for cat in result[:3]:  # Affiche les 3 premières
            print(f"  • {cat['name']} (ID: {cat['id'][:8]}...)")
        return result
    return None


def get_available_quizzes(category_id: str) -> Optional[List[Dict]]:
    """Récupère les quiz disponibles pour une catégorie"""
    print(f"\n{Colors.BOLD}=== QUIZ DISPONIBLES ==={Colors.ENDC}")
    result = api_call("GET", f"/categories/{category_id}/quizzes/available")
    if result and "data" in result:
        quizzes = result["data"]
        log(f"🎯 {len(quizzes)} quizzes trouvés", "success")
        for quiz in quizzes[:3]:
            status = "✅" if quiz.get("is_accessible") else "🔒"
            print(f"  {status} {quiz['title']} ({quiz['level']}, ID: {quiz['id'][:8]}...)")
        return quizzes
    return None


def start_quiz(quiz_id: str) -> Optional[str]:
    """Démarre un quiz et retourne l'attempt_id"""
    print(f"\n{Colors.BOLD}=== DÉMARRER QUIZ ==={Colors.ENDC}")
    result = api_call("POST", f"/attempts/start/{quiz_id}")
    if result and "attempt_id" in result:
        attempt_id = result["attempt_id"]
        quiz = result.get("quiz", {})
        questions = result.get("questions", [])
        log(f"🎯 Quiz démarré: {quiz.get('title')}", "success")
        log(f"📝 {len(questions)} questions à répondre", "info")
        return attempt_id
    return None


def save_progress(attempt_id: str, answers: List[Dict]) -> bool:
    """Sauvegarde la progression (réponses partielles)"""
    print(f"\n{Colors.BOLD}=== SAUVEGARDER PROGRESSION ==={Colors.ENDC}")
    result = api_call("POST", f"/attempts/save/{attempt_id}", {
        "answers": answers
    })
    return result is not None


def list_in_progress_attempts() -> Optional[List[Dict]]:
    """Liste les tentatives en cours"""
    print(f"\n{Colors.BOLD}=== TENTATIVES EN COURS ==={Colors.ENDC}")
    result = api_call("GET", "/attempts/in-progress")
    if result and "data" in result:
        attempts = result["data"]
        log(f"📊 {len(attempts)} tentatives en cours", "success")
        for attempt in attempts[:3]:
            print(f"  • {attempt.get('quiz_title', 'Unknown')} (ID: {attempt['attempt_id'][:8]}...)")
        return attempts
    return None


def resume_quiz(quiz_id: str) -> Optional[str]:
    """Reprend une tentative en cours"""
    print(f"\n{Colors.BOLD}=== REPRENDRE QUIZ ==={Colors.ENDC}")
    result = api_call("GET", f"/attempts/resume/{quiz_id}")
    if result and "attempt_id" in result:
        attempt_id = result["attempt_id"]
        questions = result.get("questions", [])
        log(f"↩️  Tentative reprise", "success")
        
        # Affiche les réponses déjà sélectionnées
        answered = 0
        for q in questions:
            selected = [a for a in q.get("answers", []) if a.get("user_selected")]
            if selected:
                answered += 1
        log(f"📝 {answered}/{len(questions)} questions déjà répondues", "info")
        
        return attempt_id
    return None


def submit_quiz(attempt_id: str, answers: List[Dict]) -> Optional[Dict]:
    """Soumet le quiz et obtient les résultats"""
    print(f"\n{Colors.BOLD}=== SOUMETTRE QUIZ ==={Colors.ENDC}")
    result = api_call("POST", f"/attempts/submit/{attempt_id}", {
        "answers": answers
    })
    if result:
        score = result.get("score", 0)
        passed = result.get("passed", False)
        correct = result.get("correct_answers", 0)
        total = result.get("total_questions", 0)
        
        status = "✅ RÉUSSI" if passed else "❌ ÉCHOUÉ"
        log(f"🎓 Résultats: {state} - Score: {score}% ({correct}/{total})", "success" if passed else "warning")
        return result
    return None


def get_attempt_detail(attempt_id: str) -> Optional[Dict]:
    """Récupère le détail d'une tentative"""
    print(f"\n{Colors.BOLD}=== DÉTAIL TENTATIVE ==={Colors.ENDC}")
    result = api_call("GET", f"/attempts/{attempt_id}")
    if result and "data" in result:
        data = result["data"]
        attempt = data.get("attempt", {})
        quiz = data.get("quiz", {})
        questions = data.get("questions_with_answers", [])
        
        log(f"🎯 Quiz: {quiz.get('title')}", "info")
        log(f"📊 Score: {attempt.get('score')}% - {attempt.get('passed', False)}", "success")
        return result
    return None


def main():
    """Flux de test complet"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("╔═══════════════════════════════════════════════════════╗")
    print("║  TESTS API QUIZ - SAUVEGARDE / REPRISE                ║")
    print("╚═══════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")
    
    # Données de test
    test_email = f"test_user_{int(time.time())}@example.com"
    test_password = "password123"
    test_name = "Test User"
    
    # 1. Inscription
    if not register_user(test_name, test_email, test_password):
        log("Inscription échouée, on continue quand même...", "warning")
    
    # 2. Connexion
    if not login_user(test_email, test_password):
        log("Connexion échouée!", "error")
        return
    
    # 3. Profil
    profile = get_profile()
    if profile:
        print(f"  👤 Connecté en tant que: {profile.get('name')} ({profile.get('role')})")
    
    # 4. Catégories
    categories = get_categories()
    if not categories or len(categories) == 0:
        log("Aucune catégorie trouvée", "error")
        return
    
    # Chercher la catégorie Python
    python_category = None
    for cat in categories:
        if cat["name"].lower() == "python":
            python_category = cat
            break
    
    if not python_category:
        log("Catégorie Python non trouvée, utilisation de la première", "warning")
        python_category = categories[0]
    
    category_id = python_category["id"]
    print(f"\n➡️  Sélection catégorie: {python_category['name']}")
    
    # 5. Quiz disponibles
    quizzes = get_available_quizzes(category_id)
    if not quizzes or len(quizzes) == 0:
        log("Aucun quiz disponible", "error")
        return
    
    # Trouver un quiz accessible
    quiz = None
    for q in quizzes:
        if q.get("is_accessible"):
            quiz = q
            break
    
    if not quiz:
        log("Aucun quiz accessible trouvé", "warning")
        quiz = quizzes[0]  # Prendre le premier quand même
    
    quiz_id = quiz["id"]
    print(f"➡️  Sélection quiz: {quiz['title']}")
    
    # 6. Démarrer quiz
    attempt_id = start_quiz(quiz_id)
    if not attempt_id:
        log("Erreur au démarrage du quiz", "error")
        return
    
    # 7. Sauvegarder la progression (simuler une pause)
    print(f"\n{Colors.BOLD}📝 Simulation: répondre à 2 questions et sauvegarder...{Colors.ENDC}")
    time.sleep(0.5)
    
    mock_answers = [
        {"question_id": "q1", "answer_ids": ["a1"]},
        {"question_id": "q2", "answer_ids": ["a4"]}
    ]
    
    if save_progress(attempt_id, mock_answers):
        time.sleep(1)
        
        # 8. Lister les tentatives en cours
        in_progress = list_in_progress_attempts()
        
        # 9. Reprendre la tentative
        print(f"\n{Colors.BOLD}⏸️  Simulation: reprendre après pause...{Colors.ENDC}")
        time.sleep(1)
        resumed_attempt_id = resume_quiz(quiz_id)
        
        if resumed_attempt_id:
            # 10. Soumettre le quiz (avec des réponses complètes simulées)
            print(f"\n{Colors.BOLD}📝 Simulation: compléter et soumettre le quiz...{Colors.ENDC}")
            time.sleep(0.5)
            
            # Construire un ensemble de réponses complet (exemple simplifié)
            full_answers = [
                {"question_id": "q1", "answer_ids": ["a1"]},
                {"question_id": "q2", "answer_ids": ["a4"]},
                {"question_id": "q3", "answer_ids": ["a7"]}
            ]
            
            result = submit_quiz(resumed_attempt_id, full_answers)
            
            if result:
                time.sleep(0.5)
                # 11. Détail de la tentative
                get_attempt_detail(resumed_attempt_id)
    
    print(f"\n{Colors.BOLD}{Colors.OKGREEN}")
    print("╔═══════════════════════════════════════════════════════╗")
    print("║  ✅ TESTS TERMINÉS                                    ║")
    print("╚═══════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}\n")


if __name__ == "__main__":
    main()
