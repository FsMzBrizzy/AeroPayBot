# AeroPay Bot - Telegram Gift Card Purchase Bot

A Telegram bot that allows customers to purchase gift cards from AeroElite.Shop using Visa Joker gift card numbers. The bot automates the entire checkout process including billing, shipping, and payment information.

## Features

- 🔐 Access key system for private bot access
- 💳 Gift card number processing (Visa/Joker)
- 🛒 Automated checkout on AeroElite.Shop
- 📊 Admin statistics and user management
- 🔑 Admin commands for key management and broadcasting
- ✅ Complete order flow with confirmation

## Setup

### Prerequisites

- Python 3.11+
- Telegram Bot Token (from @BotFather)
- Railway account (for deployment)
- Stripe API key (optional, for payment processing)

### Environment Variables

Create a `.env` file or set these environment variables in Railway:

```bash
# Required
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OWNER_ID=your_telegram_user_id

# Optional
BACKEND_URL=https://your-backend-url.railway.app
WEBSITE_URL=https://aeroelite.shop
STRIPE_SECRET_KEY=your_stripe_secret_key (optional)
PAYMENT_API_URL=your_payment_api_url (optional)
PORT=5000
```

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the bot:
```bash
python app/bot/main.py
```

3. Run the server (in another terminal):
```bash
python server.py
```

## Railway Deployment

### Option 1: Single Service (Recommended)

Railway will use the `Procfile` to determine what to run. You'll need to deploy two services:

1. **Bot Service**: Runs `python app/bot/main.py`
2. **Server Service**: Runs `python server.py`

### Option 2: Combined Service

You can run both in the same process by creating a combined startup script.

### Railway Setup Steps

1. Create a new Railway project
2. Add two services:
   - Service 1: Bot (worker process)
   - Service 2: Server (web process)
3. Set environment variables for both services
4. Deploy from GitHub

### Environment Variables in Railway

Set these in Railway's environment variables:

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `OWNER_ID`: Your Telegram user ID
- `BACKEND_URL`: The Railway URL of your server service
- `STRIPE_SECRET_KEY`: (Optional) Your Stripe secret key
- `PORT`: (Optional) Port for server (Railway sets this automatically)

## Usage

### For Users

1. Start the bot: `/start`
2. Enter access key (if required)
3. Choose gift card amount ($25, $50, $100, $200)
4. Enter card details:
   - 16-digit card number
   - Expiry date (MM/YY)
   - CVV
   - Cardholder name
   - Email address
   - Shipping address (street, city, state, ZIP)
   - Phone number (optional)
5. Confirm the order
6. Receive gift card codes

### Admin Commands

- `/stats` - View bot statistics
- `/broadcast` - Broadcast message to all users
- `/addkey` - Add a new access key
- `/listkeys` - List all active access keys

## Payment Integration

The bot supports multiple payment methods:

1. **Stripe** (Recommended): Set `STRIPE_SECRET_KEY` environment variable
2. **Website API**: Set `PAYMENT_API_URL` environment variable
3. **Default**: Basic validation (requires actual payment processor integration)

### Integrating with AeroElite.Shop

To integrate with your website's checkout:

1. **Option A - Stripe**: If your site uses Stripe, set the `STRIPE_SECRET_KEY` environment variable
2. **Option B - API**: If your site has a payment API, set the `PAYMENT_API_URL` and implement the API endpoint
3. **Option C - Custom**: Modify the `process_payment_default` function in `server.py` to integrate with your payment processor

## File Structure

```
AeroPayBot/
├── app/
│   └── bot/
│       └── main.py      # Telegram bot entrypoint
├── server.py           # Flask server for payment processing
├── requirements.txt    # Python dependencies
├── Procfile            # Railway deployment configuration
├── runtime.txt         # Python version
├── stats.json          # User statistics (auto-generated)
└── README.md          # This file
```

## Troubleshooting

### Bot not responding

- Check that `TELEGRAM_BOT_TOKEN` is set correctly
- Verify the bot is running (check Railway logs)
- Ensure the bot has permission to send messages

### Payment failures

- Verify `BACKEND_URL` points to your server service
- Check server logs for errors
- Ensure payment processor credentials are correct
- Verify all required fields are being sent

### Railway deployment issues

- Check that both services are running
- Verify environment variables are set in Railway
- Check Railway logs for errors
- Ensure `Procfile` is correct

## Security Notes

- Never commit `.env` file or `stats.json` to git
- Use environment variables for sensitive data
- Regularly rotate access keys
- Monitor bot usage and statistics
- Implement rate limiting for production use

## License

This project is for legitimate business use only.

## Support

For issues or questions, check the logs or contact the bot owner.

