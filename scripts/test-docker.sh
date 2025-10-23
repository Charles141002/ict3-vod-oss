#!/bin/bash

# Script de test complet pour l'application VoD Docker
echo "🧪 Test complet de l'application VoD Docker"
echo "=========================================="

echo ""
echo "📊 1. Statut des services Docker:"
docker-compose ps

echo ""
echo "📋 2. Test de l'API FastAPI:"
curl -s http://localhost:8000/api/videos | jq . 2>/dev/null || curl -s http://localhost:8000/api/videos

echo ""
echo "🌐 3. Test de l'interface web (Nginx):"
curl -s -I http://localhost/ | head -3

echo ""
echo "📱 4. Test MinIO Console:"
curl -s -I http://localhost:9001/ | head -3

echo ""
echo "🔧 5. Test MinIO API:"
curl -s http://localhost:9000/minio/health/live

echo ""
echo "📁 6. Vérification du bucket dans MinIO:"
docker exec vod-app python3 -c "
import minio
import os
client = minio.Minio('minio:9000', access_key='admin', secret_key='admin123', secure=False)
buckets = client.list_buckets()
print(f'Buckets disponibles: {[b.name for b in buckets]}')
"

echo ""
echo "✅ Tests terminés !"
echo ""
echo "🌐 Accès aux services:"
echo "  - Application VoD: http://localhost"
echo "  - FastAPI direct: http://localhost:8000"
echo "  - MinIO Console: http://localhost:9001 (admin/admin123)"
echo "  - MinIO API: http://localhost:9000"
echo ""
echo "📋 Commandes utiles:"
echo "  - Voir les logs: docker-compose logs -f"
echo "  - Arrêter: docker-compose down"
echo "  - Redémarrer: docker-compose restart"
