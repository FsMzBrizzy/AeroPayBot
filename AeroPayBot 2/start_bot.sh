#!/bin/bash

echo "🚀 Starting AeroPay Bot..."
echo ""

# Navigate to project directory
cd "$(dirname "$0")"

# Set environment variables
export TELEGRAM_BOT_TOKEN="8012296074:AAFmTtRfZFiTHnOI5Xb502QUBzwdrJRKjdE"
export OWNER_ID="5988225909"
export BACKEND_URL="http://localhost:5000"
export PORT="5000"

# Check if dependencies are installed
echo "📦 Checking dependencies..."
if ! python3 -c "import aiogram" 2>/dev/null; then
    echo "⚠️  Installing dependencies (this may take a minute)..."
    python3 -m pip install --user aiogram aiohttp flask requests python-dotenv stripe 2>&1 | grep -E "(Successfully|Requirement|ERROR)" | tail -5
fi

# Check if Flask is installed (for server)
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Installing Flask..."
    python3 -m pip install --user flask 2>&1 | grep -E "(Successfully|Requirement)" | tail -2
fi

# Kill any existing processes
echo ""
echo "🛑 Stopping any existing processes..."
pkill -f "server.py" 2>/dev/null
pkill -f "app/bot/main.py" 2>/dev/null
sleep 2

# Start server
echo "🚀 Starting server..."
nohup python3 server.py > server.log 2>&1 &
SERVER_PID=$!
echo "Server PID: $SERVER_PID"
sleep 3

# Check if server started
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Server is running on http://localhost:5000"
else
    echo "⚠️  Server may not be running. Check server.log for errors."
    tail -5 server.log 2>/dev/null
fi

# Start bot
echo ""
echo "🚀 Starting bot..."
nohup python3 app/bot/main.py > bot.log 2>&1 &
BOT_PID=$!
echo "Bot PID: $BOT_PID"
sleep 4

# Check bot status
echo ""
echo "📊 Checking bot status..."
if tail -5 bot.log 2>/dev/null | grep -qi "started\|running"; then
    echo "✅ Bot is running!"
elif tail -5 bot.log 2>/dev/null | grep -qi "error"; then
    echo "⚠️  Bot may have errors. Check bot.log:"
    tail -10 bot.log
else
    echo "📝 Bot log:"
    tail -5 bot.log 2>/dev/null
fi

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo ""
echo "📡 Server: http://localhost:5000"
echo "🤖 Bot: Check Telegram"
echo ""
echo "📝 Logs:"
echo "   - Server: tail -f server.log"
echo "   - Bot: tail -f bot.log"
echo ""
echo "🛑 To stop:"
echo "   pkill -f 'server.py'"
echo "   pkill -f 'app/bot/main.py'"
echo "=========================================="
echo ""
echo "🎉 You can now test your bot on Telegram!"
echo "   Send /start to your bot"

