#!/bin/bash

# Script pour arrêter l'application VoD Docker

echo "🛑 Arrêt de l'application VoD..."

# Arrêter les services
docker-compose down

echo "✅ Application VoD arrêtée !"
echo ""
echo "📋 Pour supprimer aussi les volumes (données MinIO):"
echo "  docker-compose down -v"
echo ""
echo "📋 Pour supprimer les images Docker:"
echo "  docker-compose down --rmi all"
