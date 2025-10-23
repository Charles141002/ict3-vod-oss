#!/bin/bash

echo "🚀 Starting ngrok for mobile access..."

# Check if ngrok is already running
if pgrep -f "ngrok http" > /dev/null; then
    echo "⚠️  ngrok is already running"
    echo "📱 Dashboard: http://localhost:4040"
    exit 0
fi

# Start ngrok
echo "🌐 Starting ngrok tunnel to localhost:8000..."
ngrok http 8000 --log=stdout &

# Wait a moment for ngrok to start
sleep 3

# Get the public URL
echo "📱 ngrok Dashboard: http://localhost:4040"
echo "🔗 Public URL will be available at the dashboard"

# Keep the script running
wait
