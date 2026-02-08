from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import router

app = FastAPI(
    title="Quiz Programming API",
    description="API Backend pour l'application de quiz de programmation",
    version="1.0.0"
)

# Configuration CORS pour permettre les requêtes depuis les applications frontend
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:8080",
        "http://localhost:3000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:3000",
        "https://backend-quiz-0ab2.onrender.com",
        "*"  # fallback (à remplacer par domaines spécifiques en production)
    ],
    allow_credentials=True,  # Permettre l'envoi de cookies/credentials
    allow_methods=["*"],   # GET, POST, PUT, DELETE, PATCH, etc.
    allow_headers=["*"],   # tous les headers
)

app.include_router(router, prefix="")
