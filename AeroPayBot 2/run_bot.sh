#!/bin/bash

# Start bot only

echo "🚀 Starting AeroPay Bot..."
echo ""

# Load environment variables if .env exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Set default backend URL
export BACKEND_URL=${BACKEND_URL:-http://localhost:5000}

echo "✅ Starting bot..."
echo "   Backend URL: $BACKEND_URL"
echo "   (Press Ctrl+C to stop)"
echo ""

python3 app/bot/main.py

