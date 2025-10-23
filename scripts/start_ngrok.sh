#!/bin/bash

# Script pour démarrer ngrok avec FastAPI
echo "🚀 Démarrage de ngrok pour VoD App..."

# Vérifier si ngrok est installé
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok n'est pas installé. Installez-le avec: brew install ngrok"
    exit 1
fi

# Démarrer ngrok sur le port 8000
echo "📡 Création du tunnel public sur le port 8000..."
ngrok http 8000

echo "✅ ngrok démarré ! Votre application est maintenant accessible publiquement."
echo "📱 Vous pouvez maintenant scanner les QR codes depuis n'importe où !"
