# 🚀 START HERE - How to Run Your Bot

## Do You Need Railway?

**Short answer**: 
- **For testing**: No, you can run locally
- **For production**: Yes, Railway is recommended (it's free and easy)

## Quick Start - Run Locally (5 minutes)

### 1. Install Python packages
```bash
cd /Users/bryce/Downloads/AeroPayBot
pip install -r requirements.txt
```

### 2. Set your bot token (in terminal)
```bash
export TELEGRAM_BOT_TOKEN="8012296074:AAFmTtRfZFiTHnOI5Xb502QUBzwdrJRKjdE"
export OWNER_ID="5988225909"
export BACKEND_URL="http://localhost:5000"
```

### 3. Open TWO terminals

**Terminal 1 - Start the server:**
```bash
cd /Users/bryce/Downloads/AeroPayBot
python server.py
```
Wait for: `Starting Flask server on port 5000...`

**Terminal 2 - Start the bot:**
```bash
cd /Users/bryce/Downloads/AeroPayBot
python app/bot/main.py
```
Wait for: `AeroPay_Bot STARTED`

### 4. Test it!
1. Open Telegram
2. Find your bot
3. Send `/start`
4. Enter key: `AERO2025VIP`

## Deploy on Railway (For 24/7 Operation)

### Why Railway?
- ✅ Free tier available
- ✅ Runs 24/7 automatically
- ✅ Easy to set up
- ✅ No need to keep your computer on

### Steps:

1. **Go to Railway**: https://railway.app
2. **Sign up** (free with GitHub)
3. **New Project** → **Deploy from GitHub**
4. **Create TWO services**:
   - Service 1: Bot (worker) - runs `python app/bot/main.py`
   - Service 2: Server (web) - runs `python server.py`
5. **Set environment variables** (see below)
6. **Deploy!**

### Environment Variables for Railway:

**Bot Service:**
```
TELEGRAM_BOT_TOKEN=8012296074:AAFmTtRfZFiTHnOI5Xb502QUBzwdrJRKjdE
OWNER_ID=5988225909
BACKEND_URL=https://your-server-url.railway.app
```

**Server Service:**
```
PORT=5000
WEBSITE_URL=https://aeroelite.shop
```

**Important**: Copy the Railway URL from your Server service and use it as `BACKEND_URL` in the Bot service!

## Which Should You Use?

| Local | Railway |
|-------|---------|
| ✅ Quick testing | ✅ 24/7 operation |
| ✅ Free | ✅ Free (with limits) |
| ❌ Stops when computer off | ✅ Always running |
| ❌ Need to keep terminal open | ✅ Automatic |

**Recommendation**: 
- Test locally first
- Then deploy to Railway for production

## Common Issues

### "Bot not responding"
- Check if both server and bot are running
- Verify `TELEGRAM_BOT_TOKEN` is correct
- Check terminal for errors

### "Can't connect to server"
- Make sure server is running first
- Check `BACKEND_URL` is correct
- On Railway: Use the Railway URL, not localhost

### "Payment failed"
- Check server logs
- Verify payment processor is configured
- Test with a valid card (if using test mode)

## Need More Help?

- See `QUICK_START.md` for detailed instructions
- See `DEPLOYMENT.md` for Railway deployment guide
- Check terminal/Railway logs for errors

## Ready to Start?

**For local testing:**
```bash
# Terminal 1
python server.py

# Terminal 2 (new terminal)
python app/bot/main.py
```

**For Railway:**
1. Push code to GitHub
2. Create Railway project
3. Set environment variables
4. Deploy!

---

**Your bot is ready to run!** 🎉

