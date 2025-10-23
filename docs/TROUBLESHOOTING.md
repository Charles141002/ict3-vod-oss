# Guide de dépannage Docker

## 🚨 Problème : Connexion Docker Hub

### Symptômes
```
failed to solve: rpc error: code = Unknown desc = failed to solve with frontend dockerfile.v0: failed to create LLB definition: failed to authorize: rpc error: code = Unknown desc = failed to fetch anonymous token: Get "https://auth.docker.io/token?scope=repository%3Alibrary%2Fpython%3Apull&service=registry.docker.io": read tcp [...]:443: read: connection reset by peer
```

### Causes possibles
- Problème de connectivité réseau vers Docker Hub
- Firewall bloquant l'accès
- Problème DNS
- Limitation de bande passante

## 🔧 Solutions

### Solution 1 : Mode développement (Recommandé)
```bash
# Démarrer MinIO seul
docker run -d -p 9000:9000 -p 9001:9001 --name vod-minio \
  -e MINIO_ROOT_USER=admin \
  -e MINIO_ROOT_PASSWORD=admin123 \
  minio/minio server /data --console-address ":9001"

# Démarrer l'application en mode développement
./scripts/dev-start.sh
```

### Solution 2 : Dockerfile simplifié
```bash
# Utiliser le Dockerfile simplifié
docker build -f Dockerfile.simple -t vod-app-simple .
```

### Solution 3 : Vérification réseau
```bash
# Tester la connectivité
ping docker.io
curl -I https://registry-1.docker.io/v2/

# Vérifier la configuration Docker
docker info
```

### Solution 4 : Proxy/VPN
Si vous êtes derrière un proxy ou VPN :
```bash
# Configurer Docker pour utiliser un proxy
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
export NO_PROXY=localhost,127.0.0.1
```

## ✅ Vérification du fonctionnement

### Services requis
1. **MinIO** : http://localhost:9000/minio/health/live
2. **Application** : http://localhost:8000/api/videos
3. **Interface** : http://localhost:8000

### Commandes de test
```bash
# Vérifier MinIO
curl http://localhost:9000/minio/health/live

# Vérifier l'API
curl http://localhost:8000/api/videos

# Vérifier l'interface
curl http://localhost:8000/
```

## 🎯 Mode de fonctionnement actuel

### Services démarrés
- ✅ **MinIO** : Container Docker (ports 9000/9001)
- ✅ **Application VoD** : Mode développement Python
- ✅ **Bucket videos** : Créé automatiquement

### Accès
- **Interface web** : http://localhost:8000
- **MinIO Console** : http://localhost:9001 (admin/admin123)
- **MinIO API** : http://localhost:9000

## 📋 Commandes utiles

### Gestion MinIO
```bash
# Démarrer MinIO
docker start vod-minio

# Arrêter MinIO
docker stop vod-minio

# Supprimer MinIO
docker rm vod-minio
```

### Gestion application
```bash
# Démarrer en mode dev
./scripts/dev-start.sh

# Arrêter l'application
Ctrl+C dans le terminal
```

### Debug
```bash
# Logs MinIO
docker logs vod-minio

# Statut containers
docker ps

# Vérifier les ports
netstat -tulpn | grep :8000
netstat -tulpn | grep :9000
```

## 🚀 Prochaines étapes

1. **Tester l'upload** : Ajouter une vidéo via l'interface
2. **Tester le streaming** : Lire une vidéo
3. **Tester les QR codes** : Scanner avec un mobile
4. **Optimiser** : Configurer ngrok si nécessaire

## 💡 Conseils

- Le mode développement est plus stable que Docker Compose
- MinIO seul en Docker + App en local = solution robuste
- Toujours vérifier la connectivité réseau avant Docker
- Utiliser les scripts fournis pour simplifier les opérations
