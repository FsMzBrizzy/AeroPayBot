# Quick Start Guide - How to Run Your Bot

## Option 1: Run Locally (For Testing)

### Step 1: Install Dependencies
```bash
cd /Users/bryce/Downloads/AeroPayBot
pip install -r requirements.txt
```

### Step 2: Set Environment Variables

Create a `.env` file in the project folder:
```bash
TELEGRAM_BOT_TOKEN=8012296074:AAFmTtRfZFiTHnOI5Xb502QUBzwdrJRKjdE
OWNER_ID=5988225909
BACKEND_URL=http://localhost:5000
PORT=5000
```

Or export them in your terminal:
```bash
export TELEGRAM_BOT_TOKEN="8012296074:AAFmTtRfZFiTHnOI5Xb502QUBzwdrJRKjdE"
export OWNER_ID="5988225909"
export BACKEND_URL="http://localhost:5000"
export PORT=5000
```

### Step 3: Run the Server (Terminal 1)
```bash
python server.py
```
You should see: `Starting Flask server on port 5000...`

### Step 4: Run the Bot (Terminal 2)
Open a new terminal and run:
```bash
python app/bot/main.py
```
You should see: `AeroPay_Bot STARTED`

### Step 5: Test the Bot
1. Open Telegram
2. Find your bot
3. Send `/start`
4. Enter access key: `AERO2025VIP`
5. Test the order flow

## Option 2: Deploy on Railway (For Production)

### Step 1: Prepare Your Code

1. **Delete old files** (optional, but recommended):
   ```bash
   rm bot.py.rtf server.py.txt README.md.txt stats.json.txt
   ```

2. **Commit to GitHub**:
   ```bash
   git add .
   git commit -m "Fixed bot code"
   git push
   ```

### Step 2: Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will detect your `Procfile` automatically

### Step 3: Create Two Services

Railway needs **TWO services**:

#### Service 1: Bot (Worker)
1. In Railway dashboard, click "New Service"
2. Select "GitHub Repo" (same repo)
3. Railway will auto-detect the `worker` command from Procfile
4. If not, set start command: `python app/bot/main.py`

#### Service 2: Server (Web)
1. Click "New Service" again
2. Select "GitHub Repo" (same repo)
3. Railway will auto-detect the `web` command from Procfile
4. If not, set start command: `python server.py`

### Step 4: Set Environment Variables

For **BOT Service**, set:
```
TELEGRAM_BOT_TOKEN=8012296074:AAFmTtRfZFiTHnOI5Xb502QUBzwdrJRKjdE
OWNER_ID=5988225909
BACKEND_URL=https://your-server-service.railway.app
```

For **SERVER Service**, set:
```
PORT=5000
WEBSITE_URL=https://aeroelite.shop
STRIPE_SECRET_KEY=your_stripe_key (optional)
```

**Important**: Get the `BACKEND_URL` from your Server service's Railway URL!

### Step 5: Deploy

1. Railway will automatically deploy when you push to GitHub
2. Check the logs for both services
3. The bot should start automatically

### Step 6: Test

1. Open Telegram
2. Find your bot
3. Send `/start`
4. Enter access key: `AERO2025VIP`
5. Test the complete flow

## Troubleshooting

### Bot Not Responding Locally
- Check that both server and bot are running
- Verify `TELEGRAM_BOT_TOKEN` is correct
- Check terminal for error messages

### Bot Not Responding on Railway
- Check Railway logs for both services
- Verify environment variables are set correctly
- Make sure `BACKEND_URL` points to your server service URL
- Check that both services are running (not crashed)

### Payment Not Working
- Verify `BACKEND_URL` is correct in bot service
- Check server logs for payment errors
- Test the health endpoint: `https://your-server-url.railway.app/health`
- Verify payment processor is configured (Stripe, etc.)

### Services Can't Communicate
- Make sure `BACKEND_URL` uses the Railway-provided URL (not localhost)
- Check that server service is publicly accessible
- Verify both services are in the same Railway project

## Quick Commands

### Local Testing
```bash
# Terminal 1 - Server
python server.py

# Terminal 2 - Bot
python app/bot/main.py
```

### Check if Running
```bash
# Test server health
curl http://localhost:5000/health

# Check bot logs
# Look for "AeroPay_Bot STARTED" in terminal
```

### Railway Logs
```bash
# View logs in Railway dashboard
# Or use Railway CLI:
railway logs
```

## Next Steps

1. ✅ Test locally first
2. ✅ Fix any issues
3. ✅ Deploy to Railway
4. ✅ Test on Railway
5. ✅ Integrate payment processor
6. ✅ Go live!

## Need Help?

- Check `DEPLOYMENT.md` for detailed deployment instructions
- Check `README.md` for full documentation
- Check Railway logs for error messages
- Verify all environment variables are set correctly

