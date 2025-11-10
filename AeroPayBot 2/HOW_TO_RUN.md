# How to Run Your Bot - Simple Answer

## Do You Need Railway?

**No, you don't NEED Railway to start!** You can test locally first.

## Option 1: Run Locally (Easiest - Test First)

### Simple Way (Using Scripts):

1. **Install dependencies** (one time):
   ```bash
   cd /Users/bryce/Downloads/AeroPayBot
   pip3 install -r requirements.txt
   ```

2. **Run the bot** (easiest method):
   ```bash
   ./run_local.sh
   ```
   This starts both server and bot automatically!

### Manual Way (Two Terminals):

**Terminal 1 - Server:**
```bash
cd /Users/bryce/Downloads/AeroPayBot
export TELEGRAM_BOT_TOKEN="8012296074:AAFmTtRfZFiTHnOI5Xb502QUBzwdrJRKjdE"
export OWNER_ID="5988225909"
export BACKEND_URL="http://localhost:5000"
python3 server.py
```

**Terminal 2 - Bot:**
```bash
cd /Users/bryce/Downloads/AeroPayBot
export TELEGRAM_BOT_TOKEN="8012296074:AAFmTtRfZFiTHnOI5Xb502QUBzwdrJRKjdE"
export OWNER_ID="5988225909"
export BACKEND_URL="http://localhost:5000"
python3 app/bot/main.py
```

### Test It:
1. Open Telegram
2. Find your bot
3. Send `/start`
4. Enter key: `AERO2025VIP`

## Option 2: Deploy on Railway (For 24/7 Running)

**Only deploy to Railway when you want the bot to run 24/7 without your computer being on.**

### Steps:

1. **Push code to GitHub**:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push
   ```

2. **Go to Railway**: https://railway.app
   - Sign up (free with GitHub)
   - Click "New Project"
   - Select "Deploy from GitHub repo"

3. **Create TWO services**:
   - **Service 1**: Bot (select "worker" or set command: `python app/bot/main.py`)
   - **Service 2**: Server (select "web" or set command: `python server.py`)

4. **Set environment variables**:

   **For Bot Service:**
   ```
   TELEGRAM_BOT_TOKEN=8012296074:AAFmTtRfZFiTHnOI5Xb502QUBzwdrJRKjdE
   OWNER_ID=5988225909
   BACKEND_URL=https://your-server-service.railway.app
   ```

   **For Server Service:**
   ```
   PORT=5000
   WEBSITE_URL=https://aeroelite.shop
   ```

5. **Deploy!** Railway will automatically deploy your code.

## Quick Comparison

| Method | When to Use | Pros | Cons |
|--------|-------------|------|------|
| **Local** | Testing | ✅ Fast, free, easy | ❌ Stops when computer off |
| **Railway** | Production | ✅ Runs 24/7, automatic | ⚠️ Need to set up (10 min) |

## Recommended Workflow

1. ✅ **Test locally first** (5 minutes)
2. ✅ **Fix any issues**
3. ✅ **Deploy to Railway** (10 minutes)
4. ✅ **Test on Railway**
5. ✅ **Go live!**

## Quick Commands

### Local Testing:
```bash
# Easy way (both at once)
./run_local.sh

# Or separately:
# Terminal 1
./run_server.sh

# Terminal 2
./run_bot.sh
```

### Check if Running:
- Server: Open http://localhost:5000/health in browser
- Bot: Send `/start` to your bot on Telegram

## Troubleshooting

### "Command not found" or "Permission denied"
```bash
chmod +x run_local.sh run_server.sh run_bot.sh
```

### "Module not found"
```bash
pip3 install -r requirements.txt
```

### "Bot not responding"
- Check both server and bot are running
- Verify `TELEGRAM_BOT_TOKEN` is correct
- Check terminal for error messages

### "Can't connect to server"
- Make sure server is running first (Terminal 1)
- Wait a few seconds after starting server
- Check `BACKEND_URL` is `http://localhost:5000`

## Summary

**To start testing RIGHT NOW:**
```bash
cd /Users/bryce/Downloads/AeroPayBot
pip3 install -r requirements.txt
./run_local.sh
```

**To deploy for 24/7 operation:**
1. Push to GitHub
2. Create Railway project
3. Set environment variables
4. Deploy!

---

**You don't need Railway to start - test locally first!** 🚀

