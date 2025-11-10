# Railway Deployment Guide

## Quick Start

### Step 1: Prepare Your Repository

1. Make sure all files are committed to GitHub
2. Remove old files (`.rtf`, `.txt` versions):
   - `bot.py.rtf` (replaced by `app/bot/main.py`)
   - `server.py.txt` (replaced by `server.py`)
   - `README.md.txt` (replaced by `README.md`)
   - `stats.json.txt` (replaced by `stats.json`)

### Step 2: Create Railway Project

1. Go to [Railway](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository

### Step 3: Configure Services

Railway needs **TWO services** for this bot:

#### Service 1: Bot Worker
1. In Railway, add a new service
2. Name it "bot" or "telegram-bot"
3. Set the start command: `python app/bot/main.py`
4. Or use the Procfile: Railway will automatically detect `worker: python app/bot/main.py`

#### Service 2: Web Server
1. Add another service in the same project
2. Name it "server" or "backend"
3. Set the start command: `python server.py`
4. Or use the Procfile: Railway will automatically detect `web: python server.py`

### Step 4: Set Environment Variables

For **BOTH services**, set these environment variables:

#### Required Variables:
```
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
OWNER_ID=your_telegram_user_id
```

#### For Bot Service:
```
BACKEND_URL=https://your-server-service-url.railway.app
```

#### For Server Service:
```
PORT=5000
WEBSITE_URL=https://aeroelite.shop
STRIPE_SECRET_KEY=your_stripe_secret_key (optional)
PAYMENT_API_URL=your_payment_api_url (optional)
```

### Step 5: Get Your Telegram User ID

1. Start a chat with [@userinfobot](https://t.me/userinfobot) on Telegram
2. It will reply with your user ID
3. Use this for the `OWNER_ID` environment variable

### Step 6: Deploy

1. Railway will automatically deploy when you push to GitHub
2. Check the logs for both services
3. The bot should start and respond to `/start`

## Troubleshooting

### Bot Not Responding

1. Check bot service logs in Railway
2. Verify `TELEGRAM_BOT_TOKEN` is correct
3. Make sure the bot service is running (not crashed)

### Server Not Responding

1. Check server service logs
2. Verify the server service is running
3. Test the health endpoint: `https://your-server-url.railway.app/health`

### Payment Not Working

1. Check server logs for payment errors
2. Verify `BACKEND_URL` in bot service points to server service
3. If using Stripe, verify `STRIPE_SECRET_KEY` is correct
4. Check that all required fields are being sent

### Services Can't Communicate

1. Make sure `BACKEND_URL` uses the Railway-provided URL
2. Check that the server service is publicly accessible
3. Verify CORS settings if needed (not required for this setup)

## Railway Configuration

### Using Procfile (Recommended)

Railway will automatically detect the Procfile:
- `web: python server.py` - Runs as web service
- `worker: python app/bot/main.py` - Runs as worker service

### Manual Configuration

If not using Procfile, set the start command in Railway:
- Bot service: `python app/bot/main.py`
- Server service: `python server.py`

### Resource Allocation

- Bot service: Minimal resources (512MB RAM is usually enough)
- Server service: Standard resources (1GB RAM recommended)

## Environment Variables Reference

| Variable | Required | Service | Description |
|----------|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | Yes | Bot | Telegram bot token from @BotFather |
| `OWNER_ID` | Yes | Bot | Your Telegram user ID |
| `BACKEND_URL` | Yes | Bot | URL of your server service |
| `PORT` | No | Server | Port for server (Railway sets this automatically) |
| `WEBSITE_URL` | No | Server | Your website URL (default: https://aeroelite.shop) |
| `STRIPE_SECRET_KEY` | No | Server | Stripe secret key for payments |
| `PAYMENT_API_URL` | No | Server | Your payment API URL |

## Testing After Deployment

1. Send `/start` to your bot on Telegram
2. Enter the access key: `AERO2025VIP`
3. Try the complete flow:
   - Choose amount
   - Enter card details
   - Enter shipping info
   - Confirm order
4. Check server logs for payment processing
5. Verify gift card codes are generated

## Monitoring

- Check Railway logs regularly
- Monitor bot response times
- Check server health endpoint: `/health`
- Review payment success/failure rates
- Monitor user statistics with `/stats` command

## Updates

To update the bot:
1. Push changes to GitHub
2. Railway will automatically redeploy
3. Check logs to verify deployment success
4. Test the bot to ensure everything works

## Support

If you encounter issues:
1. Check Railway logs first
2. Verify all environment variables are set
3. Test the health endpoint
4. Check that both services are running
5. Review the README.md for additional troubleshooting

