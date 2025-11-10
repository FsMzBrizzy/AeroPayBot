#!/bin/bash

# Start server only

echo "🚀 Starting AeroPay Bot Server..."
echo ""

# Load environment variables if .env exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Set default port
export PORT=${PORT:-5000}

echo "✅ Starting server on port $PORT..."
echo "   (Press Ctrl+C to stop)"
echo ""

python3 server.py

