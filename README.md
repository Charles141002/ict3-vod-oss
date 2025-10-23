# VoD App - Video on Demand

A complete web application for video streaming with FastAPI and MinIO.

## 🚀 Features

- **FastAPI Backend** : REST API for video management
- **HTML5 Frontend** : Modern and responsive user interface
- **Video streaming** : Direct playback from MinIO
- **Metadata management** : Video file information
- **Intuitive interface** : Modern design with statistics

## 📋 Prerequisites

- **Docker** : For the complete application (including ngrok)

### ngrok Configuration
- **Free account** : Sign up at [ngrok.com](https://ngrok.com) for a free account
- **Auth token** : Get your authtoken from the dashboard
- **Custom URL** : Optional custom subdomain for consistent access

## 🛠️ Installation

### Starting with Docker 🐳

**1. Configure ngrok (one-time setup):**
```bash
# Copy the example environment file
cp env.example .env

# Edit .env and add your ngrok token
# NGROK_AUTHTOKEN=your_token_here
```

**2. Start the complete application:**
```bash
./scripts/docker-start.sh
```

**Available services:**
- **VoD Application** : http://localhost
- **MinIO Console** : http://localhost/minio/ (admin/admin123)
- **MinIO API** : http://localhost:9000
- **ngrok Dashboard** : http://localhost:4040
- **Public URL** : https://ashely-unreflecting-franklin.ngrok-free.dev

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
│   ├── docker-start.sh # Docker startup script (includes ngrok)
│   ├── docker-stop.sh  # Docker stop script
│   └── start-ngrok.sh  # Local ngrok script (backup)
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

1. **Start the application** : `./scripts/docker-start.sh` (includes ngrok)
2. **Access QR codes** : http://localhost:8000/qr-codes
3. **Scan with mobile** : Works from anywhere via https://ashely-unreflecting-franklin.ngrok-free.dev

QR codes automatically use the public ngrok URL for optimal mobile access.

## 🛠️ Useful Scripts

- **`./scripts/docker-start.sh`** : Start the complete application with Docker (includes ngrok)
- **`./scripts/docker-stop.sh`** : Stop all Docker services
