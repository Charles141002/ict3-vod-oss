# VoD App - Video on Demand

Une application web complète pour le streaming de vidéos avec FastAPI et MinIO.

## 🚀 Fonctionnalités

- **Backend FastAPI** : API REST pour gérer les vidéos
- **Frontend HTML5** : Interface utilisateur moderne et responsive
- **Streaming vidéo** : Lecture directe depuis MinIO
- **Gestion des métadonnées** : Informations sur les fichiers vidéo
- **Interface intuitive** : Design moderne avec statistiques

## 📋 Prérequis

- Python 3.8+
- MinIO en cours d'exécution sur `localhost:9000`
- Bucket `videos` créé dans MinIO

## 🛠️ Installation

1. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

2. **Lancer l'application** :
```bash
python main.py
```

Ou avec uvicorn directement :
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 Utilisation

1. **Accéder à l'application** : http://localhost:8000
2. **API endpoints** :
   - `GET /` : Interface web principale
   - `GET /api/videos` : Liste toutes les vidéos
   - `GET /api/video/{name}` : Stream une vidéo spécifique
   - `GET /api/video/{name}/info` : Métadonnées d'une vidéo

## 📁 Structure du projet

```
ICT3/
├── main.py              # Backend FastAPI
├── requirements.txt     # Dépendances Python
├── config.env          # Configuration
├── .gitignore          # Fichiers à ignorer
├── static/
│   └── index.html      # Frontend HTML5
├── scripts/
│   ├── start_ngrok.sh  # Script ngrok
│   └── restart_server.sh # Script redémarrage
├── docs/
│   └── TECHNICAL.md    # Documentation technique
├── assets/
│   └── qr_codes/       # QR codes générés
└── data/
    └── test.mp4        # Fichier vidéo d'exemple
```

## 🎯 Fonctionnalités détaillées

### Backend (FastAPI)
- Connexion sécurisée à MinIO
- Streaming vidéo optimisé avec headers HTTP appropriés
- Gestion d'erreurs robuste
- API RESTful avec documentation automatique

### Frontend (HTML5)
- Interface responsive et moderne
- Lecteur vidéo HTML5 natif
- Liste des vidéos avec métadonnées
- Statistiques en temps réel
- Gestion d'erreurs utilisateur-friendly

## 🔧 Configuration MinIO

Assurez-vous que MinIO est configuré avec :
- **Endpoint** : `localhost:9000`
- **Access Key** : `admin`
- **Secret Key** : `admin123`
- **Bucket** : `videos` (créé et contenant vos vidéos)

## 🌐 Accès Mobile avec QR Codes

### Option 1 : Accès Local (même réseau WiFi)
1. **Lancer l'application** : `python main.py`
2. **Accéder aux QR codes** : http://localhost:8000/qr-codes
3. **Scanner avec mobile** : Fonctionne si le téléphone est sur le même WiFi

### Option 2 : Accès Public avec ngrok (recommandé)
1. **Lancer l'application** : `python main.py`
2. **Démarrer ngrok** : `./scripts/start_ngrok.sh` ou `ngrok http 8000`
3. **Accéder aux QR codes** : http://localhost:8000/qr-codes
4. **Scanner avec mobile** : Fonctionne depuis n'importe où !

## 🛠️ Scripts utiles

- **`./scripts/start_ngrok.sh`** : Démarrer ngrok pour accès public
- **`./scripts/restart_server.sh`** : Redémarrer le serveur facilement

## 🚀 Prochaines étapes

- [ ] Ajouter l'authentification utilisateur
- [ ] Implémenter le streaming HLS/DASH
- [ ] Ajouter la recherche et filtrage
- [ ] Créer un système de playlists
- [ ] Ajouter les sous-titres
- [ ] Implémenter la compression vidéo automatique
