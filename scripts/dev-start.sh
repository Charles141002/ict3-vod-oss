#!/bin/bash

# Script de démarrage alternatif sans Docker
# Pour les cas où Docker Hub n'est pas accessible

echo "🚀 Démarrage de l'application VoD en mode développement..."

# Vérifier que Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez installer Python d'abord."
    exit 1
fi

# Vérifier que pip est installé
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 n'est pas installé. Veuillez installer pip d'abord."
    exit 1
fi

# Activer l'environnement virtuel s'il existe
if [ -d "venv" ]; then
    echo "📦 Activation de l'environnement virtuel..."
    source venv/bin/activate
fi

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install -r requirements.txt

# Vérifier que MinIO est accessible
echo "🔍 Vérification de MinIO..."
if curl -f http://localhost:9000/minio/health/live 2>/dev/null; then
    echo "✅ MinIO est accessible sur localhost:9000"
    
    # Créer le bucket automatiquement
    echo "📁 Création du bucket videos..."
    python3 create_bucket.py
else
    echo "⚠️  MinIO n'est pas accessible sur localhost:9000"
    echo "📋 Pour démarrer MinIO avec Docker :"
    echo "   docker run -d -p 9000:9000 -p 9001:9001 --name minio \\"
    echo "     -e MINIO_ROOT_USER=admin \\"
    echo "     -e MINIO_ROOT_PASSWORD=admin123 \\"
    echo "     minio/minio server /data --console-address \":9001\""
    echo ""
    echo "🚀 Démarrage de l'application quand même..."
fi

# Démarrer l'application
echo "🎬 Démarrage du serveur FastAPI..."
echo "🌐 Interface web: http://localhost:8000"
echo "📱 MinIO Console: http://localhost:9001 (admin/admin123)"
echo ""
echo "📋 Pour arrêter: Ctrl+C"
echo ""

python main.py
