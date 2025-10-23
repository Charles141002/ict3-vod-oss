#!/bin/bash

# Script pour démarrer ngrok et exposer l'application VoD
echo "🚀 Démarrage de ngrok pour l'accès mobile..."

# Vérifier que ngrok est installé
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok n'est pas installé."
    echo "📋 Installation :"
    echo "  - macOS: brew install ngrok/ngrok/ngrok"
    echo "  - Linux: curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo 'deb https://ngrok-agent.s3.amazonaws.com buster main' | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok"
    echo "  - Windows: Télécharger depuis https://ngrok.com/download"
    exit 1
fi

# Vérifier que l'application est démarrée
if ! curl -f http://localhost:8000/api/videos 2>/dev/null; then
    echo "⚠️  L'application n'est pas démarrée sur le port 8000"
    echo "📋 Démarrez d'abord l'application :"
    echo "  - Docker: ./scripts/docker-start.sh"
    echo "  - Développement: ./scripts/dev-start.sh"
    exit 1
fi

echo "✅ Application détectée sur localhost:8000"
echo "🌐 Démarrage du tunnel ngrok..."

# Démarrer ngrok en arrière-plan
ngrok http 8000 --log=stdout > ngrok.log 2>&1 &
NGROK_PID=$!

# Attendre que ngrok soit prêt
echo "⏳ Attente du démarrage de ngrok..."
sleep 5

# Récupérer l'URL publique
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url' 2>/dev/null)

if [ "$NGROK_URL" != "null" ] && [ -n "$NGROK_URL" ]; then
    echo "✅ ngrok démarré avec succès !"
    echo "🌐 URL publique: $NGROK_URL"
    echo "📱 Les QR codes utiliseront maintenant cette URL"
    echo ""
    echo "📋 Pour arrêter ngrok: kill $NGROK_PID"
    echo "📋 Logs ngrok: tail -f ngrok.log"
    echo ""
    echo "🎯 Testez maintenant le scan des QR codes !"
else
    echo "❌ Impossible de récupérer l'URL ngrok"
    echo "📋 Vérifiez les logs: cat ngrok.log"
    kill $NGROK_PID 2>/dev/null
    exit 1
fi
