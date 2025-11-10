# 🚀 RUN YOUR BOT NOW - Simple Instructions

## Quick Start (Easiest Method)

### Option 1: Use the Startup Script (Recommended)

Just run this command:

```bash
cd /Users/bryce/Downloads/AeroPayBot
./start_bot.sh
```

This script will:
- ✅ Install all dependencies automatically
- ✅ Start the server
- ✅ Start the bot
- ✅ Tell you when it's ready

### Option 2: Manual Installation

If the script doesn't work, follow these steps:

#### Step 1: Install Dependencies
```bash
cd /Users/bryce/Downloads/AeroPayBot
python3 -m pip install --user aiogram aiohttp flask requests python-dotenv stripe
```

#### Step 2: Start Server (Terminal 1)
```bash
cd /Users/bryce/Downloads/AeroPayBot
export TELEGRAM_BOT_TOKEN="8012296074:AAFmTtRfZFiTHnOI5Xb502QUBzwdrJRKjdE"
export OWNER_ID="5988225909"
export BACKEND_URL="http://localhost:5000"
export PORT="5000"
python3 server.py
```

#### Step 3: Start Bot (Terminal 2 - NEW TERMINAL WINDOW)
```bash
cd /Users/bryce/Downloads/AeroPayBot
export TELEGRAM_BOT_TOKEN="8012296074:AAFmTtRfZFiTHnOI5Xb502QUBzwdrJRKjdE"
export OWNER_ID="5988225909"
export BACKEND_URL="http://localhost:5000"
python3 app/bot/main.py
```

## ✅ When Ready

You'll know it's ready when you see:
- Server: `Starting Flask server on port 5000...`
- Bot: `AeroPay_Bot STARTED`

## 🧪 Test Your Bot

1. Open Telegram
2. Find your bot
3. Send `/start`
4. Enter access key: `AERO2025VIP`
5. Test the order flow!

## 🛑 To Stop

Press `Ctrl+C` in both terminal windows, or:
```bash
pkill -f server.py
pkill -f app/bot/main.py
```

## ❌ Troubleshooting

### "Module not found" error
```bash
python3 -m pip install --user aiogram aiohttp flask requests python-dotenv stripe
```

### "Permission denied" for script
```bash
chmod +x start_bot.sh
```

### Bot not responding
- Check that both server and bot are running
- Check the logs: `tail -f bot.log` and `tail -f server.log`
- Verify `TELEGRAM_BOT_TOKEN` is correct

### Server not responding
- Check: `curl http://localhost:5000/health`
- Should return: `{"status": "ok", ...}`
- Check logs: `tail -f server.log`

## 📞 Need Help?

Check the logs:
- Server: `tail -f server.log`
- Bot: `tail -f bot.log`

---

**Ready to start? Run: `./start_bot.sh`** 🚀

