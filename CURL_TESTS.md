# Tests cURL — Endpoints de Quiz & Sauvegarde/Reprise

**Base URL:** `https://backend-quiz-0ab2.onrender.com` (adapter selon votre environnement)

## 1. Authentification

### Inscription
```bash
curl -X POST https://backend-quiz-0ab2.onrender.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Connexion (récupère le token dans la réponse + cookie HTTP-only)
```bash
curl -X POST https://backend-quiz-0ab2.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

**Note:** L'option `-c cookies.txt` sauvegarde le cookie. L'option `-b cookies.txt` le réutilise ensuite.

### Récupérer profil (utilise le cookie)
```bash
curl -X GET https://backend-quiz-0ab2.onrender.com/auth/me \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

---

## 2. Catégories & Quiz

### Charger catégories
```bash
curl -X GET https://backend-quiz-0ab2.onrender.com/categories \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

### Charger quiz disponibles d'une catégorie (avec accès selon progression)
**Note:** Récupérez d'abord une `category_id` de la requête précédente.
```bash
curl -X GET "https://backend-quiz-0ab2.onrender.com/categories/{category_id}/quizzes/available" \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

---

## 3. Démarrer un Quiz

**Note:** Récupérez un `quiz_id` de la requête catégories.

```bash
curl -X POST "https://backend-quiz-0ab2.onrender.com/attempts/start/{quiz_id}" \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Réponse :**
```json
{
  "attempt_id": "uuid...",
  "quiz": { "id": "...", "title": "...", "level": "debutant", ... },
  "questions": [
    {
      "id": "...",
      "question_text": "Question 1?",
      "order": 1,
      "answers": [
        { "id": "answer_id_1", "answer_text": "Réponse A", "order": 1 },
        { "id": "answer_id_2", "answer_text": "Réponse B", "order": 2 }
      ]
    }
  ]
}
```

Sauvegardez l'`attempt_id` pour les étapes suivantes.

---

## 4. Sauvegarder la Progression (pause)

**Endpoint:** `POST /attempts/save/{attempt_id}`

Sauvegarde les réponses partielles (sans soumettre le quiz).

```bash
curl -X POST "https://backend-quiz-0ab2.onrender.com/attempts/save/{attempt_id}" \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "answers": [
      {
        "question_id": "q1_id",
        "answer_ids": ["answer_id_1", "answer_id_3"]
      },
      {
        "question_id": "q2_id",
        "answer_ids": ["answer_id_5"]
      }
    ]
  }'
```

**Réponse:**
```json
{ "message": "Progress saved" }
```

---

## 5. Lister les Tentatives en Cours

**Endpoint:** `GET /attempts/in-progress`

Voir toutes les tentatives non terminées de l'utilisateur.

```bash
curl -X GET https://backend-quiz-0ab2.onrender.com/attempts/in-progress \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Réponse:**
```json
{
  "data": [
    {
      "attempt_id": "uuid...",
      "quiz_id": "quiz_id_1",
      "quiz_title": "Python - Débutant",
      "score": null,
      "passed": null,
      "completed_at": null
    }
  ]
}
```

---

## 6. Reprendre un Quiz (avec réponses sauvegardées)

**Endpoint:** `GET /attempts/resume/{quiz_id}`

Récupère la tentative en cours avec les réponses préalablement sélectionnées (marquées `user_selected: true`).

```bash
curl -X GET "https://backend-quiz-0ab2.onrender.com/attempts/resume/{quiz_id}" \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Réponse:**
```json
{
  "attempt_id": "uuid...",
  "quiz": { "id": "...", "title": "Python - Débutant", ... },
  "questions": [
    {
      "id": "q1_id",
      "question_text": "Quel est...",
      "order": 1,
      "answers": [
        { "id": "a1", "answer_text": "Réponse A", "order": 1, "user_selected": true },
        { "id": "a2", "answer_text": "Réponse B", "order": 2, "user_selected": false }
      ]
    }
  ]
}
```

---

## 7. Soumettre le Quiz (final)

**Endpoint:** `POST /attempts/submit/{attempt_id}`

Soumet toutes les réponses et calcule le score final. Marque la tentative comme complétée.

```bash
curl -X POST "https://backend-quiz-0ab2.onrender.com/attempts/submit/{attempt_id}" \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "answers": [
      {
        "question_id": "q1_id",
        "answer_ids": ["answer_id_1"]
      },
      {
        "question_id": "q2_id",
        "answer_ids": ["answer_id_5", "answer_id_6"]
      },
      {
        "question_id": "q3_id",
        "answer_ids": ["answer_id_9"]
      }
    ]
  }'
```

**Réponse:**
```json
{
  "score": 75.5,
  "passed": false,
  "correct_answers": 7,
  "total_questions": 10,
  "details": [
    {
      "question_id": "q1_id",
      "question_text": "Question 1?",
      "user_answers": ["answer_id_1"],
      "correct_answers": ["answer_id_1"],
      "is_correct": true
    }
  ]
}
```

---

## 8. Voir l'Historique des Tentatives

```bash
curl -X GET https://backend-quiz-0ab2.onrender.com/users/me/attempts \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

### Voir le détail d'une tentative
```bash
curl -X GET "https://backend-quiz-0ab2.onrender.com/attempts/{attempt_id}" \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

---

## Flux Complet d'Exemple

### 1. Login
```bash
TOKEN=$(curl -s -X POST https://backend-quiz-0ab2.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"email":"john@example.com","password":"password123"}' | jq -r '.access_token')
echo "Token: $TOKEN"
```

### 2. Get category ID
```bash
CATEGORY_ID=$(curl -s -X GET https://backend-quiz-0ab2.onrender.com/categories \
  -H "Content-Type: application/json" \
  -b cookies.txt | jq -r '.[0].id')
echo "Category ID: $CATEGORY_ID"
```

### 3. Get quiz ID
```bash
QUIZ_ID=$(curl -s -X GET "https://backend-quiz-0ab2.onrender.com/categories/$CATEGORY_ID/quizzes/available" \
  -H "Content-Type: application/json" \
  -b cookies.txt | jq -r '.data[0].id')
echo "Quiz ID: $QUIZ_ID"
```

### 4. Start quiz
```bash
ATTEMPT_ID=$(curl -s -X POST "https://backend-quiz-0ab2.onrender.com/attempts/start/$QUIZ_ID" \
  -H "Content-Type: application/json" \
  -b cookies.txt | jq -r '.attempt_id')
echo "Attempt ID: $ATTEMPT_ID"
```

### 5. Save progress (pause)
```bash
curl -X POST "https://backend-quiz-0ab2.onrender.com/attempts/save/$ATTEMPT_ID" \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"answers":[{"question_id":"q1","answer_ids":["a1"]}]}'
```

### 6. List in-progress
```bash
curl -s -X GET https://backend-quiz-0ab2.onrender.com/attempts/in-progress \
  -H "Content-Type: application/json" \
  -b cookies.txt | jq '.'
```

### 7. Resume quiz
```bash
curl -s -X GET "https://backend-quiz-0ab2.onrender.com/attempts/resume/$QUIZ_ID" \
  -H "Content-Type: application/json" \
  -b cookies.txt | jq '.'
```

### 8. Submit quiz
```bash
curl -X POST "https://backend-quiz-0ab2.onrender.com/attempts/submit/$ATTEMPT_ID" \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "answers": [
      {"question_id":"q1","answer_ids":["a1"]},
      {"question_id":"q2","answer_ids":["a5"]}
    ]
  }'
```

---

## Notes Importantes

1. **Cookies vs Bearer Token:**
   - Utilisez `-c cookies.txt` pour sauvegarder le cookie à la connexion
   - Utilisez `-b cookies.txt` pour envoyer le cookie dans les requêtes suivantes
   - Ou passez le `access_token` reçu en header: `-H "Authorization: Bearer $TOKEN"`

2. **PowerShell (sur Windows):**
   ```powershell
   $response = Invoke-WebRequest -Uri "https://backend-quiz-0ab2.onrender.com/auth/login" `
     -Method POST `
     -Headers @{"Content-Type"="application/json"} `
     -Body '{"email":"john@example.com","password":"password123"}' `
     -SessionVariable session
   
   # Cookies sont maintenant dans $session, à réutiliser après
   $next = Invoke-WebRequest -Uri "https://backend-quiz-0ab2.onrender.com/auth/me" `
     -Method GET `
     -WebSession $session
   ```

3. **Vérifier les réponses:**
   - Ajoutez `| jq '.'` pour formater le JSON (si `jq` est installé)
   - Ou piquez simplement le résultat brut

---

Bon test! 🎯
