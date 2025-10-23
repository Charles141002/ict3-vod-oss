#!/bin/bash

# Script pour construire et démarrer l'application VoD avec Docker

echo "🐳 Construction et démarrage de l'application VoD..."

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez installer Docker d'abord."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez installer Docker Compose d'abord."
    exit 1
fi

# Construire l'image
echo "🔨 Construction de l'image Docker..."
docker-compose build

# Démarrer les services
echo "🚀 Démarrage des services..."
docker-compose up -d

# Attendre que les services soient prêts
echo "⏳ Attente du démarrage des services..."
sleep 10

# Vérifier le statut
echo "📊 Statut des services:"
docker-compose ps

echo ""
echo "✅ Application VoD démarrée !"
echo "🌐 Interface web: http://localhost"
echo "📱 MinIO Console: http://localhost/minio/"
echo "🔧 MinIO API: http://localhost:9000"
echo ""
echo "📋 Commandes utiles:"
echo "  - Voir les logs: docker-compose logs -f"
echo "  - Arrêter: docker-compose down"
echo "  - Redémarrer: docker-compose restart"
echo "  - Reconstruire: docker-compose up --build"
