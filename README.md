# VoD App - Video on Demand

A complete web application for video streaming with FastAPI and MinIO.

## 🚀 Features

- **FastAPI Backend** : REST API for video management
- **HTML5 Frontend** : Modern and responsive user interface
- **Video streaming** : Direct playback from MinIO
- **Metadata management** : Video file information
- **Intuitive interface** : Modern design with statistics

## 📋 Prerequisites

- **Docker** : For the complete application
- **ngrok** : For mobile access (optional)

### Installing ngrok

**macOS :**
```bash
brew install ngrok/ngrok/ngrok
```

**Linux :**
```bash
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo 'deb https://ngrok-agent.s3.amazonaws.com buster main' | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok
```

**Windows :**
Download from [ngrok.com/download](https://ngrok.com/download)

## 🛠️ Installation

### Starting with Docker 🐳

**1. Start the application:**
```bash
./scripts/docker-start.sh
```

**2. Start ngrok for mobile access:**
```bash
./scripts/start-ngrok.sh
```

**Available services:**
- **VoD Application** : http://localhost
- **MinIO Console** : http://localhost/minio/ (admin/admin123)
- **MinIO API** : http://localhost:9000
- **ngrok Dashboard** : http://localhost:4040

## 🌐 Usage

1. **Access the application** : http://localhost:8000
2. **API endpoints** :
   - `GET /` : Main web interface
   - `GET /api/videos` : List all videos
   - `GET /api/video/{name}` : Stream a specific video
   - `GET /api/video/{name}/info` : Video metadata

## 📁 Project Structure

```
ICT3/
├── main.py              # FastAPI Backend
├── requirements.txt     # Python Dependencies
├── create_bucket.py     # Automatic bucket creation
├── Dockerfile          # Docker application image
├── docker-compose.yml  # Docker orchestration
├── nginx.conf          # Nginx configuration
├── static/
│   └── index.html      # HTML5 Frontend
├── scripts/
│   ├── docker-start.sh # Docker startup script
│   ├── docker-stop.sh  # Docker stop script
│   └── start-ngrok.sh  # ngrok script for mobile
├── assets/
│   └── qr_codes/       # Generated QR codes (empty)
├── README.md           # Main documentation
└── SUBMISSION.md       # Submission report
```

## 🎯 Detailed Features

### Backend (FastAPI)
- Secure connection to MinIO
- Optimized video streaming with appropriate HTTP headers
- Robust error handling
- RESTful API with automatic documentation

### Frontend (HTML5)
- Modern responsive interface
- Native HTML5 video player
- Video list with metadata
- Real-time statistics
- User-friendly error handling

## 🔧 MinIO Configuration

Make sure MinIO is configured with:
- **Endpoint** : `localhost:9000`
- **Access Key** : `admin`
- **Secret Key** : `admin123`
- **Bucket** : `videos` (created and containing your videos)

## 📱 Mobile Access with QR Codes

**To scan QR codes with your mobile:**

1. **Start ngrok** : `./scripts/start-ngrok.sh`
2. **Access QR codes** : http://localhost:8000/qr-codes
3. **Scan with mobile** : Works from anywhere!

QR codes automatically use the public ngrok URL for optimal mobile access.

## 🛠️ Useful Scripts

- **`./scripts/docker-start.sh`** : Start the complete application with Docker
- **`./scripts/docker-stop.sh`** : Stop all Docker services
- **`./scripts/start-ngrok.sh`** : Start ngrok for mobile access
