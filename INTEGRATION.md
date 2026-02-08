# Documentation d'intégration — Backend Quiz

Cette documentation explique comment intégrer le backend (auth via cookie HTTP-only) depuis des clients web et mobiles. Elle est focalisée sur l'authentification : le token JWT est stocké dans un cookie HTTP-only nommé `access_token`, et le backend accepte aussi le header `Authorization: Bearer <token>`.

**Fichiers de référence**
- [app/services/auth.py](app/services/auth.py#L1-L200)
- [app/api/router.py](app/api/router.py#L1-L300)
- [app/main.py](app/main.py#L1-L200)

**Résumé du flux d'auth**
- POST `/auth/login` : vérifie email/mdp, crée un JWT via `create_access_token` et :
  - écrit un cookie HTTP-only `access_token` (attributs : `httponly=True`, `samesite=None`, `secure=False` en dev)
  - renvoie aussi le `access_token` et `user_id` dans le corps (utile pour mobile)
- Middleware/dépendance `get_current_user` lit d'abord le cookie `access_token`, puis, si absent, le header `Authorization: Bearer ...`.
- GET `/auth/me` : endpoint protégé qui utilise `get_current_user`.
- POST `/auth/logout` : supprime le cookie `access_token`.

Conséquence pratique : les applications web peuvent s'appuyer sur le cookie HTTP-only (navigateur envoie le cookie automatiquement si la requête inclut les credentials), et les applications mobiles peuvent utiliser la valeur renvoyée dans le corps (`access_token`) et l'ajouter au header `Authorization`.

---

**1) Intégration Web (navigateur / SPA)**

Points clés
- Le cookie est HTTP-only : JavaScript ne peut pas lire directement `access_token`.
- Pour que le navigateur envoie le cookie sur des requêtes cross-origin il faut :
  - côté serveur : activer `allow_credentials=True` et lister explicitement `allow_origins` (ne pas utiliser `"*"`)
  - côté client (fetch/axios) : envoyer les credentials (`credentials: 'include'` ou `withCredentials: true`).

Serveur — modifications recommandées
- Dans `app/main.py`, remplacez la configuration CORS par :

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mon-frontend.example.com"],  # mettre vos origines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

- En production, dans `response.set_cookie` (voir `app/api/router.py`), utilisez `secure=True` et `samesite='None'` pour permettre cross-site sur HTTPS.

Client — exemples
- Login (fetch) :

```javascript
fetch('https://api.example.com/auth/login', {
  method: 'POST',
  credentials: 'include', // envoie/stocke les cookies cross-site
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
})
.then(r => r.json())
```

- Requêtes authentifiées ensuite :

```javascript
fetch('https://api.example.com/auth/me', {
  method: 'GET',
  credentials: 'include'
})
```

- Axios global config :

```javascript
import axios from 'axios';
const api = axios.create({ baseURL: 'https://api.example.com', withCredentials: true });
```

CSRF
- Parce que vous utilisez des cookies (automatiquement envoyés), protégez vos endpoints contre le CSRF pour toute requête qui modifie l'état (POST/PUT/DELETE). Options :
  - Implémenter un token anti-CSRF (double submit). À la connexion, renvoyer un token non-HTTP-only lisible par JS (ou header) que le client enverra dans un header `X-CSRF-Token` pour les requêtes mutantes.
  - Conserver `SameSite=Lax` si possible pour réduire la surface, mais si vous avez besoin de cross-site (ex : frontend hébergé sur un domaine différent), utilisez `SameSite=None` + `Secure` + token CSRF.

---

**2) Intégration Mobile (iOS / Android / React Native)**

Contraintes
- Les navigateurs mobiles gèrent les cookies comme précédemment, mais les apps natives n'envoient pas automatiquement un cookie set par une réponse HTTP dans le même sens qu'un navigateur (cela dépend de la librairie HTTP et de la gestion des cookies).

Recommandations pratiques
- Option A (recommandée) — Utiliser le token renvoyé dans la réponse JSON et stocker ce token dans un stockage sécurisé de la plateforme (Keychain sur iOS, EncryptedSharedPreferences / Keystore sur Android) :
  - Au login, backend renvoie `access_token` dans le corps (c'est déjà fait).
  - Le client mobile stocke ce token en secure storage et l'envoie ensuite dans `Authorization: Bearer <token>` pour chaque requête.
  - Avantage : simple, pas de gestion de cookie sur mobile.
  - Exemple (React Native / fetch) :

```javascript
// après login
const token = responseJson.access_token;
await SecureStore.setItemAsync('access_token', token); // ex: expo-secure-store

// pour requêtes authentifiées
const token = await SecureStore.getItemAsync('access_token');
fetch('https://api.example.com/auth/me', {
  headers: { 'Authorization': `Bearer ${token}` }
})
```

- Option B — gérer les cookies côté mobile : possible via des bibliothèques (ex: react-native-cookies), mais plus fragile; l'approche header Bearer est plus portable.

Sécurité mobile
- Stockez les tokens dans un stockage sécurisé (Keychain/Keystore).
- Préférez tokens courts et un mécanisme de refresh (refresh token stocké aussi de façon sécurisée) plutôt que de longues durées d'access token.

---

**3) Recommandations de sécurité et production**
- Toujours servir via HTTPS et définir `secure=True` pour les cookies en production.
- Ne pas utiliser `allow_origins=["*"]` quand `allow_credentials=True` — cela doit être une liste d'origines explicitement autorisées.
- Mettre `httponly=True` sur le cookie (déjà le cas) pour éviter le vol via XSS.
- Implémenter CSRF tokens si vous utilisez les cookies pour l'authentification web.
- Utiliser des access tokens courts (ex : 15 min) + refresh tokens pour renouveler l'accès.
- Considérer d'avoir le refresh token en cookie HTTP-only et l'access token renvoyé au mobile dans le corps (pour protéger refresh tokens côté navigateur et mobile différemment).

---

**4) Modifications serveur suggérées (patch minimal)**
- `app/main.py` : définir `allow_credentials=True` et remplacer `allow_origins` par la liste d'origines frontales.
- `app/api/router.py` : à passer `secure=True` dans `set_cookie` en production.
- Ajouter un endpoint `POST /auth/refresh` si vous mettez en place refresh tokens.

---

**5) Tests & Debugging**
- Pour tester depuis un navigateur en local : ouvrir la console réseau et vérifier que les entêtes `Set-Cookie` sont présents dans la réponse login, et que les requêtes suivantes incluent bien le cookie.
- Pour tester mobile (option A) : vérifier que l'app reçoit `access_token` dans le corps et l'envoie dans `Authorization`.
- Avec Postman :
  - Vous pouvez simuler navigateur en acceptant et renvoyant les cookies.
  - Ou ajoutez manuellement `Authorization: Bearer <token>` si vous testez la variante header.

