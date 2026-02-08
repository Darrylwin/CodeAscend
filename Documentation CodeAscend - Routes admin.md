## Vue d'ensemble

Cette API REST permet de gérer une plateforme de quiz de programmation avec système de progression par niveaux, authentification utilisateur et tableau de bord administrateur.

### Informations générales

- **URL de base**: `http://127.0.0.1:8000`
- **Format**: JSON
- **Authentification**: JWT (JSON Web Token) via cookies HTTP-only ou header Authorization
- **Version**: 1.0.0

---

##  Authentification

L'API utilise JWT pour l'authentification. Deux méthodes sont supportées :

1. **Cookies HTTP-only** (recommandé) : Le token est automatiquement inclus dans les requêtes
2. **Header Authorization** : `Authorization: Bearer <token>`

### Configuration CORS

```javascript
// Configuration actuelle (développement)
allow_origins: ["*"]
allow_credentials: false
allow_methods: ["*"]
allow_headers: ["*"]
```

**Important** : En production, restreindre les origines autorisées.

---

## 📋 Endpoints par catégorie

### 1. Authentification

#### POST `/auth/login`

**Connexion utilisateur**

**Body (JSON)**:

```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**Réponse succès (200)**:

```json
{
  "access_token": "jwt-token-string",
  "token_type": "bearer",
  "user_id": "uuid-string"
}
```

**Cookies définis**:

- `access_token`: JWT token (HTTP-only, expire après 30 minutes)

**Erreurs possibles**:

- `401`: Email ou mot de passe incorrect

**Note**: Le cookie HTTP-only est automatiquement défini et sera inclus dans les requêtes suivantes.

---

#### GET `/auth/me`

**Récupérer les informations de l'utilisateur connecté**

**Headers requis**:

```
Authorization: Bearer <token>
```

OU le cookie `access_token` doit être présent

**Réponse succès (200)**:

```json
{
  "id": "uuid-string",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "user",
  "created_at": "2025-02-07T10:30:00Z",
  "updated_at": "2025-02-07T10:30:00Z"
}
```

**Rôles possibles**:

- `user`: Utilisateur standard
- `admin`: Administrateur

**Erreurs possibles**:

- `401`: Token manquant ou invalide

---

#### PUT `/auth/me`

**Modifier le profil de l'utilisateur connecté**

**Headers requis**:

```
Authorization: Bearer <token>
```

**Body (JSON)**:

```json
{
  "name": "John Smith",
  "email": "john.smith@example.com",
  "old_password": "password123",
  "new_password": "newpassword456"
}
```

**Champs**:

- `name` (optionnel): Nouveau nom
- `email` (optionnel): Nouvel email
- `old_password` (requis): Mot de passe actuel pour vérification
- `new_password` (optionnel): Nouveau mot de passe

**Réponse succès (200)**:

```json
{
  "id": "uuid-string",
  "name": "John Smith",
  "email": "john.smith@example.com",
  "role": "user",
  "created_at": "2025-02-07T10:30:00Z",
  "updated_at": "2025-02-07T12:45:00Z"
}
```

**Erreurs possibles**:

- `400`: Ancien mot de passe incorrect ou email déjà utilisé
- `401`: Non authentifié

---

#### POST `/auth/logout`

**Déconnexion utilisateur**

**Headers requis**:

```
Authorization: Bearer <token>
```

**Réponse succès (200)**:

```json
{
  "message": "Déconnexion réussie"
}
```

**Note**: Supprime le cookie `access_token`.

---

### 2. Catégories

#### GET `/categories`

**Liste toutes les catégories**

**Headers requis**:

```
Authorization: Bearer <token>
```

**Query parameters**:

- `is_active` (optionnel): `true` ou `false` pour filtrer par statut

**Réponse succès (200)**:

```json
[
  {
    "id": "uuid-string",
    "name": "JavaScript",
    "description": "Apprenez les bases de JavaScript",
    "icon_url": "https://example.com/js-icon.png",
    "is_active": true,
    "created_at": "2025-02-07T10:30:00Z",
    "updated_at": "2025-02-07T10:30:00Z"
  }
]
```

**Note**:

- Les utilisateurs standards ne voient que les catégories actives
- Les admins voient toutes les catégories

---

#### POST `/categories`

**Créer une nouvelle catégorie** (Admin uniquement)

**Headers requis**:

```
Authorization: Bearer <token>
```

**Body (JSON)**:

```json
{
  "name": "Python",
  "description": "Maîtrisez Python",
  "icon_url": "https://example.com/python-icon.png",
  "is_active": true
}
```

**Réponse succès (200)**:

```json
{
  "id": "uuid-string",
  "name": "Python",
  "description": "Maîtrisez Python",
  "icon_url": "https://example.com/python-icon.png",
  "is_active": true,
  "created_at": "2025-02-07T10:30:00Z",
  "updated_at": null
}
```

**Erreurs possibles**:

- `400`: Nom de catégorie déjà existant
- `403`: Non autorisé (non admin)

---

#### GET `/categories/{category_id}`

**Récupérer une catégorie spécifique**

**Headers requis**:

```
Authorization: Bearer <token>
```

**Réponse succès (200)**:

```json
{
  "id": "uuid-string",
  "name": "JavaScript",
  "description": "Apprenez les bases de JavaScript",
  "icon_url": "https://example.com/js-icon.png",
  "is_active": true,
  "created_at": "2025-02-07T10:30:00Z",
  "updated_at": "2025-02-07T10:30:00Z"
}
```

**Erreurs possibles**:

- `404`: Catégorie non trouvée

---

#### PUT `/categories/{category_id}`

**Modifier une catégorie** (Admin uniquement)

**Headers requis**:

```
Authorization: Bearer <token>
```

**Body (JSON)**:

```json
{
  "name": "JavaScript ES6+",
  "description": "JavaScript moderne",
  "icon_url": "https://example.com/js-icon-new.png",
  "is_active": true
}
```

**Réponse succès (200)**:

```json
{
  "id": "uuid-string",
  "name": "JavaScript ES6+",
  "description": "JavaScript moderne",
  "icon_url": "https://example.com/js-icon-new.png",
  "is_active": true,
  "created_at": "2025-02-07T10:30:00Z",
  "updated_at": "2025-02-07T14:00:00Z"
}
```

**Erreurs possibles**:

- `403`: Non autorisé (non admin)
- `404`: Catégorie non trouvée

---

#### DELETE `/categories/{category_id}`

**Supprimer une catégorie** (Admin uniquement)

**Headers requis**:

```
Authorization: Bearer <token>
```

**Réponse succès (200)**:

```json
{
  "message": "Category deleted"
}
```

**Erreurs possibles**:

- `400`: Impossible de supprimer une catégorie avec des quiz associés
- `403`: Non autorisé (non admin)
- `404`: Catégorie non trouvée

---

#### GET `/categories/{category_id}/quizzes/available`

**Récupérer les quiz disponibles pour une catégorie avec logique d'accès**

**Headers requis**:

```
Authorization: Bearer <token>
```

**Réponse succès (200)**:

```json
{
  "data": [
    {
      "id": "uuid-string",
      "title": "Les bases de JavaScript",
      "level": "debutant",
      "category_id": "uuid-string",
      "status": "published",
      "is_accessible": true
    },
    {
      "id": "uuid-string-2",
      "title": "JavaScript Avancé",
      "level": "intermediaire",
      "category_id": "uuid-string",
      "status": "published",
      "is_accessible": false
    }
  ],
  "meta": {},
  "message": "Quiz disponibles récupérés avec succès"
}
```

**Logique d'accessibilité**:

- **Niveau débutant** : Toujours accessible
- **Niveau intermédiaire** : Accessible si un quiz débutant de cette catégorie est réussi avec ≥ 80%
- **Niveau avancé** : Accessible si un quiz intermédiaire de cette catégorie est réussi avec ≥ 80%

**Erreurs possibles**:

- `404`: Catégorie non trouvée

---

### 3. Quiz

#### GET `/quizzes`

**Liste tous les quiz**

**Headers requis**:

```
Authorization: Bearer <token>
```

**Query parameters**:

- `category_id` (optionnel): Filtrer par catégorie
- `level` (optionnel): `debutant`, `intermediaire`, `avance`
- `status` (optionnel): `draft`, `published`

**Réponse succès (200)**:

```json
[
  {
    "id": "uuid-string",
    "category_id": "uuid-string",
    "title": "Les bases de JavaScript",
    "level": "debutant",
    "status": "published",
    "created_at": "2025-02-07T10:30:00Z",
    "updated_at": "2025-02-07T10:30:00Z"
  }
]
```

**Niveaux disponibles**:

- `debutant`
- `intermediaire`
- `avance`

**Statuts disponibles**:

- `draft`: Brouillon
- `published`: Publié

**Note**: Les utilisateurs standards ne voient que les quiz publiés.

---

#### POST `/quizzes`

**Créer un nouveau quiz** (Admin uniquement)

**Headers requis**:

```
Authorization: Bearer <token>
```

**Body (JSON)**:

```json
{
  "category_id": "uuid-string",
  "title": "Quiz Python Débutant",
  "level": "debutant",
  "status": "draft"
}
```

**Réponse succès (200)**:

```json
{
  "id": "uuid-string",
  "category_id": "uuid-string",
  "title": "Quiz Python Débutant",
  "level": "debutant",
  "status": "draft",
  "created_at": "2025-02-07T10:30:00Z",
  "updated_at": null
}
```

**Erreurs possibles**:

- `403`: Non autorisé (non admin)
- `404`: Catégorie non trouvée

---

#### GET `/quizzes/{quiz_id}`

**Récupérer un quiz spécifique**

**Headers requis**:

```
Authorization: Bearer <token>
```

**Réponse succès (200)**:

```json
{
  "id": "uuid-string",
  "category_id": "uuid-string",
  "title": "Les bases de JavaScript",
  "level": "debutant",
  "status": "published",
  "created_at": "2025-02-07T10:30:00Z",
  "updated_at": "2025-02-07T10:30:00Z"
}
```

**Erreurs possibles**:

- `404`: Quiz non trouvé ou non publié (pour les utilisateurs standards)

---

#### PUT `/quizzes/{quiz_id}`

**Modifier un quiz** (Admin uniquement)

**Headers requis**:

```
Authorization: Bearer <token>
```

**Body (JSON)**:

```json
{
  "title": "JavaScript - Les Bases",
  "level": "debutant",
  "status": "published"
}
```

**Réponse succès (200)**:

```json
{
  "id": "uuid-string",
  "category_id": "uuid-string",
  "title": "JavaScript - Les Bases",
  "level": "debutant",
  "status": "published",
  "created_at": "2025-02-07T10:30:00Z",
  "updated_at": "2025-02-07T14:00:00Z"
}
```

**Erreurs possibles**:

- `403`: Non autorisé (non admin)
- `404`: Quiz non trouvé

---

#### DELETE `/quizzes/{quiz_id}`

**Supprimer un quiz** (Admin uniquement)

**Headers requis**:

```
Authorization: Bearer <token>
```

**Réponse succès (200)**:

```json
{
  "message": "Quiz deleted"
}
```

**Erreurs possibles**:

- `400`: Impossible de supprimer un quiz avec des tentatives
- `403`: Non autorisé (non admin)
- `404`: Quiz non trouvé

---

### 4. Questions

#### GET `/questions`

**Liste toutes les questions** (Admin uniquement)

**Headers requis**:

```
Authorization: Bearer <token>
```

**Query parameters**:

- `quiz_id` (optionnel): Filtrer par quiz

**Réponse succès (200)**:

```json
[
  {
    "id": "uuid-string",
    "quiz_id": "uuid-string",
    "question_text": "Qu'est-ce qu'une variable ?",
    "order": 1,
    "created_at": "2025-02-07T10:30:00Z",
    "answers": [
      {
        "id": "uuid-string",
        "question_id": "uuid-string",
        "answer_text": "Un conteneur pour stocker des données",
        "is_correct": true,
        "order": 1,
        "created_at": "2025-02-07T10:30:00Z"
      }
    ]
  }
]
```

**Erreurs possibles**:

- `403`: Non autorisé (non admin)

---

#### POST `/questions`

**Créer une nouvelle question avec ses réponses** (Admin uniquement)

**Headers requis**:

```
Authorization: Bearer <token>
```

**Body (JSON)**:

```json
{
  "quiz_id": "uuid-string",
  "question_text": "Qu'est-ce qu'une variable ?",
  "order": 1,
  "answers": [
    {
      "answer_text": "Un conteneur pour stocker des données",
      "is_correct": true,
      "order": 1
    },
    {
      "answer_text": "Une fonction",
      "is_correct": false,
      "order": 2
    },
    {
      "answer_text": "Une boucle",
      "is_correct": false,
      "order": 3
    }
  ]
}
```

**Réponse succès (200)**:

```json
{
  "id": "uuid-string",
  "quiz_id": "uuid-string",
  "question_text": "Qu'est-ce qu'une variable ?",
  "order": 1,
  "created_at": "2025-02-07T10:30:00Z",
  "answers": [
    {
      "id": "uuid-string",
      "question_id": "uuid-string",
      "answer_text": "Un conteneur pour stocker des données",
      "is_correct": true,
      "order": 1,
      "created_at": "2025-02-07T10:30:00Z"
    }
  ]
}
```

**Note**: Une question peut avoir plusieurs réponses correctes (QCM).

**Erreurs possibles**:

- `400`: Ordre déjà utilisé pour ce quiz
- `403`: Non autorisé (non admin)
- `404`: Quiz non trouvé

---

#### POST `/quizzes/{quiz_id}/questions`

**Ajouter une question à un quiz spécifique** (Admin uniquement)

**Headers requis**:

```
Authorization: Bearer <token>
```

**Body (JSON)**:

```json
{
  "question_text": "Quel est le résultat de 2 + 2 ?",
  "order": 2,
  "answers": [
    {
      "answer_text": "4",
      "is_correct": true,
      "order": 1
    },
    {
      "answer_text": "5",
      "is_correct": false,
      "order": 2
    }
  ]
}
```

**Réponse succès (200)**:

```json
{
  "id": "uuid-string",
  "quiz_id": "uuid-string",
  "question_text": "Quel est le résultat de 2 + 2 ?",
  "order": 2,
  "created_at": "2025-02-07T10:30:00Z",
  "answers": [
    {
      "id": "uuid-string",
      "question_id": "uuid-string",
      "answer_text": "4",
      "is_correct": true,
      "order": 1,
      "created_at": "2025-02-07T10:30:00Z"
    }
  ]
}
```

**Erreurs possibles**:

- `400`: Ordre déjà utilisé pour ce quiz
- `403`: Non autorisé (non admin)
- `404`: Quiz non trouvé

---

#### GET `/questions/{question_id}`

**Récupérer une question spécifique** (Admin uniquement)

**Headers requis**:

```
Authorization: Bearer <token>
```

**Réponse succès (200)**:

```json
{
  "id": "uuid-string",
  "quiz_id": "uuid-string",
  "question_text": "Qu'est-ce qu'une variable ?",
  "order": 1,
  "created_at": "2025-02-07T10:30:00Z",
  "answers": [
    {
      "id": "uuid-string",
      "question_id": "uuid-string",
      "answer_text": "Un conteneur pour stocker des données",
      "is_correct": true,
      "order": 1,
      "created_at": "2025-02-07T10:30:00Z"
    }
  ]
}
```

**Erreurs possibles**:

- `403`: Non autorisé (non admin)
- `404`: Question non trouvée

---

#### PUT `/questions/{question_id}`

**Modifier une question et ses réponses** (Admin uniquement)

**Headers requis**:

```
Authorization: Bearer <token>
```

**Body (JSON)**:

```json
{
  "question_text": "Qu'est-ce qu'une variable en JavaScript ?",
  "order": 1,
  "answers": [
    {
      "answer_text": "Un conteneur pour stocker des valeurs",
      "is_correct": true,
      "order": 1
    },
    {
      "answer_text": "Une fonction",
      "is_correct": false,
      "order": 2
    }
  ]
}
```

**Note**: Les anciennes réponses sont supprimées et remplacées par les nouvelles.

**Réponse succès (200)**:

```json
{
  "id": "uuid-string",
  "quiz_id": "uuid-string",
  "question_text": "Qu'est-ce qu'une variable en JavaScript ?",
  "order": 1,
  "created_at": "2025-02-07T10:30:00Z",
  "answers": [
    {
      "id": "uuid-string-new",
      "question_id": "uuid-string",
      "answer_text": "Un conteneur pour stocker des valeurs",
      "is_correct": true,
      "order": 1,
      "created_at": "2025-02-07T14:00:00Z"
    }
  ]
}
```

**Erreurs possibles**:

- `400`: Ordre déjà utilisé pour ce quiz
- `403`: Non autorisé (non admin)
- `404`: Question non trouvée

---

#### DELETE `/questions/{question_id}`

**Supprimer une question** (Admin uniquement)

**Headers requis**:

```
Authorization: Bearer <token>
```

**Réponse succès (200)**:

```json
{
  "message": "Question deleted"
}
```

**Erreurs possibles**:

- `400`: Impossible de supprimer une question avec des réponses utilisateur
- `403`: Non autorisé (non admin)
- `404`: Question non trouvée

---

### 7. Administration

#### GET `/admin/stats`

**Récupérer les statistiques globales de la plateforme** (Admin uniquement)

**Headers requis**:

```
Authorization: Bearer <token>
```

**Réponse succès (200)**:

```json
{
  "total_users": 150,
  "total_quizzes": 45,
  "total_categories": 8,
  "popular_quizzes": [
    {
      "title": "Les bases de JavaScript",
      "attempts": 235,
      "avg_score": 78.5
    },
    {
      "title": "Python pour débutants",
      "attempts": 198,
      "avg_score": 82.3
    }
  ],
  "success_rates": {
    "debutant": {
      "avg_score": 82.5,
      "success_rate": 75.3
    },
    "intermediaire": {
      "avg_score": 71.8,
      "success_rate": 58.2
    },
    "avance": {
      "avg_score": 65.4,
      "success_rate": 42.1
    }
  }
}
```

**Données fournies**:

- `total_users`: Nombre total d'utilisateurs
- `total_quizzes`: Nombre total de quiz
- `total_categories`: Nombre total de catégories
- `popular_quizzes`: Top 5 des quiz les plus joués avec leur score moyen
- `success_rates`: Statistiques par niveau (score moyen et taux de réussite)

**Erreurs possibles**:

- `403`: Non autorisé (non admin)

---

#### GET `/admin/users`

**Liste paginée des utilisateurs** (Admin uniquement)

**Headers requis**:

```
Authorization: Bearer <token>
```

**Query parameters**:

- `search` (optionnel): Recherche par nom ou email
- `page` (optionnel, défaut: 1): Numéro de page
- `per_page` (optionnel, défaut: 10): Nombre d'utilisateurs par page

**Réponse succès (200)**:

```json
{
  "data": [
    {
      "id": "uuid-string",
      "name": "John Doe",
      "email": "john@example.com",
      "role": "user",
      "created_at": "2025-02-07T10:30:00Z"
    }
  ],
  "meta": {
    "total": 150,
    "page": 1,
    "per_page": 10,
    "total_pages": 15
  }
}
```

**Exemple de recherche**:

```
GET /admin/users?search=john&page=1&per_page=20
```

**Erreurs possibles**:

- `403`: Non autorisé (non admin)

---

#### GET `/admin/users/stats`

**Statistiques détaillées de tous les utilisateurs** (Admin uniquement)

**Headers requis**:

```
Authorization: Bearer <token>
```

**Réponse succès (200)**:

```json
[
  {
    "id": "uuid-string",
    "name": "John Doe",
    "email": "john@example.com",
    "attempts_count": 15,
    "avg_score": 78.5,
    "passed_quizzes": 10,
    "categories_mastered": 3,
    "created_at": "2025-02-07T10:30:00Z"
  }
]
```

**Erreurs possibles**:

- `403`: Non autorisé (non admin)

---

#### GET `/admin/users/{user_id}`

**Récupérer un utilisateur spécifique** (Admin uniquement)

**Headers requis**:

```
Authorization: Bearer <token>
```

**Réponse succès (200)**:

```json
{
  "id": "uuid-string",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "user",
  "created_at": "2025-02-07T10:30:00Z",
  "updated_at": "2025-02-07T10:30:00Z"
}
```

**Erreurs possibles**:

- `403`: Non autorisé (non admin)
- `404`: Utilisateur non trouvé

---

#### PUT `/admin/users/{user_id}`

**Modifier un utilisateur** (Admin uniquement)

**Headers requis**:

```
Authorization: Bearer <token>
```

**Body (JSON)**:

```json
{
  "name": "John Smith",
  "email": "john.smith@example.com",
  "role": "admin"
}
```

**Réponse succès (200)**:

```json
{
  "id": "uuid-string",
  "name": "John Smith",
  "email": "john.smith@example.com",
  "role": "admin",
  "created_at": "2025-02-07T10:30:00Z",
  "updated_at": "2025-02-07T14:00:00Z"
}
```

**Erreurs possibles**:

- `400`: Email déjà utilisé par un autre utilisateur
- `403`: Non autorisé (non admin)
- `404`: Utilisateur non trouvé

---

#### DELETE `/admin/users/{user_id}`

**Supprimer un utilisateur** (Admin uniquement)

**Headers requis**:

```
Authorization: Bearer <token>
```

**Réponse succès (200)**:

```json
{
  "message": "User deleted successfully"
}
```

**Données supprimées en cascade**:

- Toutes les réponses utilisateur
- Toutes les tentatives de quiz
- Tous les enregistrements de progression

**Erreurs possibles**:

- `400`: Impossible de supprimer son propre compte
- `403`: Non autorisé (non admin)
- `404`: Utilisateur non trouvé

---

## 📊 Modèles de données

### User

```typescript
{
  id: string;                    // UUID
  name: string;
  email: string;
  role: "user" | "admin";
  created_at: string;            // ISO 8601
  updated_at: string | null;     // ISO 8601
}
```

### Category

```typescript
{
  id: string;                    // UUID
  name: string;
  description: string | null;
  icon_url: string | null;
  is_active: boolean;
  created_at: string;            // ISO 8601
  updated_at: string | null;     // ISO 8601
}
```

### Quiz

```typescript
{
  id: string;                    // UUID
  category_id: string;           // UUID
  title: string;
  level: "debutant" | "intermediaire" | "avance";
  status: "draft" | "published";
  created_at: string;            // ISO 8601
  updated_at: string | null;     // ISO 8601
}
```

### Question

```typescript
{
  id: string;                    // UUID
  quiz_id: string;               // UUID
  question_text: string;
  order: number;                 // Position dans le quiz
  created_at: string;            // ISO 8601
  answers: Answer[];
}
```

### Answer

```typescript
{
  id: string;                    // UUID
  question_id: string;           // UUID
  answer_text: string;
  is_correct: boolean;           // Non retourné lors du démarrage du quiz
  order: number;
  created_at: string;            // ISO 8601
}
```

---

## Gestion des erreurs

### Format des réponses d'erreur

```json
{
  "detail": "Message d'erreur descriptif"
}
```

### Codes HTTP utilisés

|Code|Signification|Utilisation|
|---|---|---|
|200|OK|Requête réussie|
|400|Bad Request|Données invalides ou contrainte violée|
|401|Unauthorized|Non authentifié ou token invalide|
|403|Forbidden|Authentifié mais non autorisé (droits insuffisants)|
|404|Not Found|Ressource non trouvée|
|500|Internal Server Error|Erreur serveur|

---

## Logique métier importante

### 1. Système de progression par niveaux

La progression est basée sur un système à 3 niveaux par catégorie :

1. **Niveau débutant** : Toujours accessible
2. **Niveau intermédiaire** : Débloqué après avoir réussi un quiz débutant avec ≥ 80%
3. **Niveau avancé** : Débloqué après avoir réussi un quiz intermédiaire avec ≥ 80%

### 2. Calcul du score

- Score = (Réponses correctes / Total questions) × 100
- Une réponse est correcte si **toutes** les cases cochées correspondent exactement aux bonnes réponses
- Seuil de réussite : **80%**

### 3. Questions à choix multiples (QCM)

- Une question peut avoir plusieurs réponses correctes
- L'utilisateur peut sélectionner plusieurs réponses
- La validation est stricte : il faut sélectionner **exactement** les bonnes réponses

### 4. Tentatives multiples

- Un utilisateur peut refaire un quiz autant de fois qu'il le souhaite
- Si une tentative est déjà en cours (non complétée), elle est retournée au lieu d'en créer une nouvelle
- Chaque tentative complétée est enregistrée dans l'historique

### 5. Mise à jour de la progression

La progression n'est mise à jour que si :

- Le quiz est **réussi** (score ≥ 80%)
- Le niveau du quiz est **supérieur** au niveau actuel de l'utilisateur dans cette catégorie

---

## Conseils d'intégration frontend

### 1. Gestion de l'authentification

```javascript
// Configuration de fetch pour inclure les cookies
const apiCall = async (endpoint, options = {}) => {
  const response = await fetch(`http://127.0.0.1:8000${endpoint}`, {
    ...options,
    credentials: 'include', // Important pour les cookies HTTP-only
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    }
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }
  
  return response.json();
};

// Ou avec header Authorization
const apiCallWithToken = async (endpoint, token, options = {}) => {
  const response = await fetch(`http://127.0.0.1:8000${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers
    }
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }
  
  return response.json();
};
```

### 3. Vérification des droits d'accès

```javascript
// Vérifier si l'utilisateur est admin
const user = await apiCall('/auth/me');
const isAdmin = user.role === 'admin';

// Afficher/masquer les éléments admin dans l'UI
if (isAdmin) {
  // Afficher le bouton "Administration"
}
```

### 4. Gestion de la pagination (liste utilisateurs)

```javascript
const loadUsers = async (page = 1, search = '') => {
  const params = new URLSearchParams({ page, per_page: 20 });
  if (search) params.append('search', search);
  
  const response = await apiCall(`/admin/users?${params}`);
  
  return {
    users: response.data,
    pagination: response.meta
  };
};
```

### 5. Affichage de la progression

```javascript
// Récupérer la progression de l'utilisateur
const progress = await apiCall('/users/me/progress');

// Afficher le niveau atteint par catégorie
progress.forEach(p => {
  console.log(`${p.category.name}: Niveau ${p.current_level}`);
});
```

---

## Compte de test

Pour tester l'API, utilisez ces identifiants :

**Administrateur**:

- Email: `admin@test.com`
- Mot de passe: `admin123`

---

## Notes importantes

1. **CORS** : L'API est configurée pour accepter toutes les origines en développement (`allow_origins: ["*"]`). En production, restreindre à vos domaines.
    
2. **Cookies HTTP-only** : Le token JWT est stocké dans un cookie HTTP-only pour plus de sécurité. Il expire après 30 minutes.
    
3. **Validation stricte des QCM** : Pour qu'une question soit considérée comme correcte, l'utilisateur doit sélectionner **exactement** les bonnes réponses (ni plus, ni moins).
    
4. **Tentatives incomplètes** : Si un utilisateur démarre un quiz mais ne le soumet pas, la tentative reste en cours. Au prochain démarrage du même quiz, il récupère la tentative existante.
    
5. **Suppression en cascade** : La suppression d'un utilisateur supprime aussi toutes ses données (tentatives, réponses, progression).
    
6. **Ordre des questions/réponses** : Les questions et réponses sont triées par leur champ `order` pour maintenir la cohérence.
    

---

## Exemples d'utilisation

### Exemple complet avec React

```javascript
import { useState, useEffect } from 'react';

const API_BASE = 'http://127.0.0.1:8000';

function QuizApp() {
  const [user, setUser] = useState(null);
  const [categories, setCategories] = useState([]);
  
  // Connexion
  const login = async (email, password) => {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    
    if (response.ok) {
      const data = await response.json();
      // Récupérer les infos utilisateur
      const userResponse = await fetch(`${API_BASE}/auth/me`, {
        credentials: 'include'
      });
      setUser(await userResponse.json());
    }
  };
  
  // Charger les catégories
  useEffect(() => {
    if (user) {
      fetch(`${API_BASE}/categories`, { credentials: 'include' })
        .then(res => res.json())
        .then(setCategories);
    }
  }, [user]);
  
  return (
    <div>
      {!user ? (
        <LoginForm onLogin={login} />
      ) : (
        <Dashboard user={user} categories={categories} />
      )}
    </div>
  );
}
```

### Support

Pour toute question ou problème d'intégration, consultez :

- Le code source : `/d/quiz-backend`
- L'application de test HTML : `/d/quiz-backend/html-test/index.html`

---

## Changelog

### Version 1.0.0 (Février 2025)

- API initiale avec tous les endpoints fonctionnels
- Système d'authentification JWT
- Gestion des quiz multi-niveaux
- Système de progression par catégorie
- Dashboard administrateur
- Documentation complète

---

_Documentation générée le 07 février 2025_