#!/usr/bin/env python3
"""
Serveur simple pour l'application de test HTML
Utilisation: python server.py
Puis ouvrir http://localhost:8080 dans le navigateur
"""

import http.server
import socketserver
import os

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Ajouter les headers CORS pour permettre les requêtes vers l'API
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == '__main__':
    print(f"🚀 Serveur de test démarré sur http://localhost:{PORT}")
    print(f"📁 Sert les fichiers depuis: {DIRECTORY}")
    print("💡 Ouvrez http://localhost:8080 dans votre navigateur")
    print("💡 L'API est déployée sur https://backend-quiz-0ab2.onrender.com")

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Serveur arrêté")
            httpd.shutdown()