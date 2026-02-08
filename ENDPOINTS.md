**Documentation d'intégration — Endpoints API**

- **But**: fournir une référence pratique pour intégrer tous les endpoints du backend (méthode, path, auth, corps attendu, exemples web/mobile).
- **Cookie auth**: le JWT est stocké dans un cookie HTTP-only `access_token`. Le backend accepte aussi `Authorization: Bearer <token>`.

**Général**
- Base URL: `https://api.example.com` (adapter selon environnement)
- Cookie: `access_token` (HTTP-only)
- Header alternatif: `Authorization: Bearer <token>`
- Endpoints publics: `GET /health`, `POST /auth/register`, `POST /auth/login`.
- Tous les autres endpoints nécessitent l'authentification (`get_current_user`). Certaines routes demandent `role=admin`.

**Authentification**
- POST /auth/register
  - Auth: non
  - Body: `UserCreate` (ex: `{ "name": "...", "email": "...", "password": "..." }`)
  - Response: message + `user_id`
- POST /auth/login
  - Auth: non
  - Body: `UserLogin` (ex: `{ "email": "...", "password": "..." }`)
  - Effets: définit cookie HTTP-only `access_token`; renvoie aussi `{ access_token, token_type, user_id }`
- GET /auth/me
  - Auth: oui
  - Response: `UserResponse` (profil courant)
- PUT /auth/me
  - Auth: oui
  - Body: `UserProfileUpdate` (ancien mot de passe, changements souhaités)
- POST /auth/logout
  - Auth: non requis (supprime cookie si présent)

**Health**
- GET /health
  - Auth: non
  - Usage: vérification simple de disponibilité

**Categories** (prefixe `/categories`)
- GET /categories/
  - Auth: oui
  - Query: `is_active` optionnel
  - Rôle: si non-admin, retourne uniquement `is_active == True`
- POST /categories/
  - Auth: oui, **admin**
  - Body: `CategoryCreate`
- GET /categories/{category_id}
  - Auth: oui
  - Rôle: non-admin ne voit pas les catégories inactives
- PUT /categories/{category_id}
  - Auth: oui, **admin**
  - Body: `CategoryUpdate`
- DELETE /categories/{category_id}
  - Auth: oui, **admin**
- GET /categories/{category_id}/quizzes/available
  - Auth: oui
  - Retourne la liste des quizzes visibles et un flag `is_accessible` selon progression utilisateur

**Quizzes** (prefixe `/quizzes`)
- GET /quizzes/
  - Auth: oui
  - Query: `category_id`, `level`, `status`
  - Non-admin voit seulement `status == "published"`
- POST /quizzes/
  - Auth: oui, **admin**
  - Body: `QuizCreate`
- GET /quizzes/{quiz_id}
  - Auth: oui
  - Non-admin ne voit que `published`
- PUT /quizzes/{quiz_id}
  - Auth: oui, **admin**
- DELETE /quizzes/{quiz_id}
  - Auth: oui, **admin**
- POST /quizzes/{quiz_id}/questions
  - Auth: oui, **admin**
  - Body: `QuestionCreateForQuiz` (question + answers)

**Questions** (prefixe `/questions`)
- GET /questions/
  - Auth: oui, **admin**
  - Query: `quiz_id` optionnel
- POST /questions/
  - Auth: oui, **admin**
  - Body: `QuestionCreate` (avec `answers`)
- GET /questions/{question_id}
  - Auth: oui, **admin**
- PUT /questions/{question_id}
  - Auth: oui, **admin**
  - Body: `QuestionUpdate` (remplace réponses existantes)
- DELETE /questions/{question_id}
  - Auth: oui, **admin**

**Attempts (tentatives)** (prefixe `/attempts`)
- POST /attempts/start/{quiz_id}
  - Auth: oui
  - Démarre une tentative; crée ou renvoie une `attempt_id` et les questions (sans indiquer l'is_correct)
- POST /attempts/submit/{attempt_id}
  - Auth: oui
  - Body: `QuizSubmit` (liste des réponses de l'utilisateur)
  - Retourne `score`, `passed`, `details`
- GET /attempts/progress
  - Auth: oui
  - Retourne progression par catégorie
- GET /attempts/attempts
  - Auth: oui
  - Historique des tentatives utilisateur
- GET /attempts/{attempt_id}
  - Auth: oui
  - Détail d'une tentative (questions + quelles réponses l'utilisateur a choisies)

**Users** (prefixe `/users`)
- GET /users/me/stats
  - Auth: oui
  - Statistiques utilisateur (nombre tentatives, score moyen, récentes)
- GET /users/me/attempts
  - Auth: oui
  - Alias pour `/attempts/attempts`
- GET /users/me/progress
  - Auth: oui
  - Alias pour `/attempts/progress`

**Admin** (prefixe `/admin`) — accès `role=admin` requis
- GET /admin/stats
  - Auth: admin
  - Statistiques globales (users, quizzes, catégories, top quizzes)
- GET /admin/users
  - Auth: admin
  - Query: `search`, `page`, `per_page`
- GET /admin/users/stats
  - Auth: admin
  - Statistiques détaillées par utilisateur
- GET /admin/users/{user_id}
  - Auth: admin
- PUT /admin/users/{user_id}
  - Auth: admin
  - Body: `UserUpdate`
- DELETE /admin/users/{user_id}
  - Auth: admin
  - Supprime aussi tentatives / réponses / progrès associés

---

**Exemples d'utilisation**

1) Web (cookie HTTP-only) — login + requête protégée
- Login (fetch) :

```javascript
fetch('https://api.example.com/auth/login', {
  method: 'POST',
  credentials: 'include', // IMPORTANT pour stocker le cookie cross-site
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
})
.then(r => r.json()).then(console.log)
```

- Requête authentifiée (cookie envoyé automatiquement si `credentials: 'include'`):

```javascript
fetch('https://api.example.com/auth/me', {
  method: 'GET',
  credentials: 'include'
})
```

2) Mobile / API clients (Bearer header)
- Après login, utiliser le `access_token` renvoyé dans le JSON et le stocker en secure storage. Pour chaque requête :

```javascript
fetch('https://api.example.com/auth/me', {
  headers: { 'Authorization': `Bearer ${token}` }
})
```

3) cURL (tester header)

```bash
# login pour obtenir token (ici on suppose que la réponse contient access_token)
curl -X POST -H "Content-Type: application/json" -d '{"email":"u@e.com","password":"pwd"}' https://api.example.com/auth/login

# appel avec header
curl -H "Authorization: Bearer <token>" https://api.example.com/quizzes
```

**Notes importantes / recommandations**
- Pour l'intégration Web cross-origin : activer `allow_credentials=True` côté serveur et définir explicitement `allow_origins` (ne pas utiliser `*`), puis utiliser `credentials: 'include'` côté client.
- Protéger les endpoints mutateurs contre CSRF si vous utilisez les cookies pour l'authentification. Options : token anti-CSRF (double submit) ou header custom envoyé par le client après login.
- En production : `response.set_cookie(..., secure=True, samesite='None', httponly=True)` et HTTPS obligatoire.
- Mobile : stocker l'access token dans un stockage sécurisé (Keychain / Keystore), préférer `Authorization: Bearer` pour la simplicité.

