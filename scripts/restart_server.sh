#!/bin/bash

# Script pour redémarrer le serveur VoD App
echo "🔄 Redémarrage du serveur VoD App..."

# Arrêter le serveur existant
echo "⏹️ Arrêt du serveur existant..."
pkill -f "python main.py" 2>/dev/null || true

# Attendre un peu
sleep 2

# Démarrer le nouveau serveur
echo "🚀 Démarrage du nouveau serveur..."
python main.py &

echo "✅ Serveur redémarré !"
echo "🌐 Accédez à l'application : http://localhost:8000"
echo "📚 Documentation API : http://localhost:8000/docs"
