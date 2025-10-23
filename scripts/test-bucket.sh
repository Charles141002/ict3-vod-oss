#!/bin/bash

# Script de test pour vérifier la création automatique du bucket
echo "🧪 Test de la création automatique du bucket..."

# Tester le script Python directement
echo "📋 Test 1: Script Python standalone"
python3 create_bucket.py

echo ""
echo "📋 Test 2: Vérification via API"
curl -s http://localhost:8000/api/videos | jq .

echo ""
echo "📋 Test 3: Vérification MinIO Console"
echo "🌐 Accéder à: http://localhost:9001"
echo "👤 Login: admin / admin123"
echo "📁 Bucket: videos"

echo ""
echo "✅ Tests terminés !"
