#!/bin/bash

# Quick start script for local development

echo "🚀 Starting AeroPay Bot Locally..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating one..."
    echo "TELEGRAM_BOT_TOKEN=8012296074:AAFmTtRfZFiTHnOI5Xb502QUBzwdrJRKjdE" > .env
    echo "OWNER_ID=5988225909" >> .env
    echo "BACKEND_URL=http://localhost:5000" >> .env
    echo "PORT=5000" >> .env
    echo "✅ Created .env file"
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if dependencies are installed
echo "📦 Checking dependencies..."
if ! python3 -c "import aiogram" 2>/dev/null; then
    echo "⚠️  Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo ""
echo "✅ Starting server on port 5000..."
echo "   (Press Ctrl+C to stop)"
echo ""

# Start server in background
python3 server.py &
SERVER_PID=$!

# Wait a moment for server to start
sleep 2

echo "✅ Starting bot..."
echo "   (Press Ctrl+C to stop)"
echo ""

# Start bot (foreground)
python3 app/bot/main.py

# Cleanup on exit
kill $SERVER_PID 2>/dev/null
echo ""
echo "👋 Bot stopped"

