# VoD App 🎬

A simple Video on Demand project that allows you to upload, stream videos, and generate QR codes to watch them on mobile.

## 🚀 Quick Start

1.  **Prerequisites**:
    *   Have Docker and Docker Compose installed.
    *   **Important**: Create an account on [ngrok.com](https://ngrok.com) and get your authtoken so QR codes work on mobile.

2.  **Configuration**:
    *   Copy the example file: `cp env.example .env`
    *   Add your token in the `.env` file: `NGROK_AUTHTOKEN=your_token_here`

3.  **Start**:
    ```bash
    ./scripts/docker-start.sh
    ```
    *Or simply `docker-compose up --build`*

4.  **Access**:
    *   Web App: [http://localhost:8000](http://localhost:8000)
    *   MinIO Console (Storage): [http://localhost:9001](http://localhost:9001) (Login: `admin` / Pass: `admin123`)

## ⚙️ How it works

1.  **Storage**: Videos are stored in a **MinIO** bucket (S3 compatible).
2.  **Streaming**: The **FastAPI** backend streams videos in chunks to avoid loading everything into memory. It handles "Range Requests" to allow seeking forward/backward in the video.
3.  **Mobile Access**: **Ngrok** creates a secure tunnel to your local PC, allowing generation of QR codes scannable from any smartphone (even on 4G).

## 🛠 Tech Stack

*   **Backend**: Python + FastAPI (fast & async)
*   **Storage**: MinIO (S3 Object Storage)
*   **Containerization**: Docker & Docker Compose
*   **Tools**:
    *   `qrcode`: QR code generation
    *   `ngrok`: Internet exposure for mobile testing
    *   `uvicorn`: ASGI Server

## ✨ Features

*   Video upload (drag & drop)
*   Smooth video streaming (supports Range requests)
*   Automatic QR Code generation
*   Supports all browsers (Chrome, Firefox, Safari, Mobile)
