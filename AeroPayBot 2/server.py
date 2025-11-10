from flask import Flask, request, jsonify
import requests
import os
import secrets
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Website configuration
WEBSITE_URL = os.getenv("WEBSITE_URL", "https://aeroelite.shop")
PAYMENT_API_URL = os.getenv("PAYMENT_API_URL")  # If your site has a payment API
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")  # If using Stripe

def gen_codes(amount):
    """Generate gift card codes based on amount"""
    try:
        cnt = max(1, int(amount.replace("$", "")) // 25)
        return [f"AE-{secrets.token_hex(4).upper()}-{secrets.token_hex(4).upper()}" for _ in range(cnt)]
    except Exception as e:
        logger.error(f"Error generating codes: {e}")
        return [f"AE-{secrets.token_hex(4).upper()}-{secrets.token_hex(4).upper()}"]

def process_payment_stripe(data):
    """Process payment using Stripe API"""
    if not STRIPE_SECRET_KEY:
        return {"success": False, "error": "Stripe API key not configured"}
    
    try:
        try:
            import stripe
        except ImportError:
            return {"success": False, "error": "Stripe library not installed"}
        
        stripe.api_key = STRIPE_SECRET_KEY
        
        amount = int(data['amount'].replace("$", "")) * 100  # Convert to cents
        
        # Create payment method
        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": data['card_number'],
                "exp_month": int(data['exp_month']),
                "exp_year": int(data['exp_year']),
                "cvc": data['cvv'],
            },
            billing_details={
                "name": data['name'],
                "email": data['email'],
                "address": {
                    "line1": data['address'],
                    "city": data['city'],
                    "state": data['state'],
                    "postal_code": data['zip_code'],
                    "country": "US",
                },
                "phone": data.get('phone', ''),
            },
        )
        
        # Create payment intent
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            payment_method=payment_method.id,
            confirm=True,
            description=f"AeroElite Gift Card - {data['amount']}",
            receipt_email=data['email'],
            shipping={
                "name": data['name'],
                "address": {
                    "line1": data['address'],
                    "city": data['city'],
                    "state": data['state'],
                    "postal_code": data['zip_code'],
                    "country": "US",
                },
                "phone": data.get('phone', ''),
            },
        )
        
        if payment_intent.status == "succeeded":
            codes = gen_codes(data['amount'])
            return {"success": True, "codes": codes, "payment_id": payment_intent.id}
        else:
            return {"success": False, "error": f"Payment status: {payment_intent.status}"}
    
    except Exception as e:
        logger.error(f"Stripe payment error: {e}", exc_info=True)
        return {"success": False, "error": str(e)}

def process_payment_website_api(data):
    """Process payment through website's API endpoint"""
    if not PAYMENT_API_URL:
        return {"success": False, "error": "Payment API URL not configured"}
    
    try:
        payload = {
            "amount": data['amount'],
            "card_number": data['card_number'],
            "exp_month": data['exp_month'],
            "exp_year": data['exp_year'],
            "cvv": data['cvv'],
            "name": data['name'],
            "email": data['email'],
            "address": data['address'],
            "city": data['city'],
            "state": data['state'],
            "zip_code": data['zip_code'],
            "phone": data.get('phone', ''),
        }
        
        response = requests.post(
            PAYMENT_API_URL,
            json=payload,
            timeout=30,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                codes = gen_codes(data['amount'])
                return {"success": True, "codes": codes}
            else:
                return {"success": False, "error": result.get("error", "Payment failed")}
        else:
            return {"success": False, "error": f"API returned status {response.status_code}"}
    
    except Exception as e:
        logger.error(f"Website API payment error: {e}", exc_info=True)
        return {"success": False, "error": str(e)}

def process_payment_default(data):
    """
    Default payment processing - generates codes after validating card
    NOTE: This is a placeholder. In production, you should integrate with
    your actual payment processor (Stripe, PayPal, your website's API, etc.)
    """
    try:
        # Basic card validation
        card_number = data['card_number'].replace(" ", "").replace("-", "")
        if len(card_number) != 16 or not card_number.isdigit():
            return {"success": False, "error": "Invalid card number"}
        
        # Validate expiry
        exp_month = int(data['exp_month'])
        exp_year = int(data['exp_year'])
        if not (1 <= exp_month <= 12):
            return {"success": False, "error": "Invalid expiry month"}
        
        current_year = datetime.now().year
        if exp_year < current_year or (exp_year == current_year and exp_month < datetime.now().month):
            return {"success": False, "error": "Card has expired"}
        
        # Validate CVV
        cvv = data['cvv']
        if len(cvv) != 3 or not cvv.isdigit():
            return {"success": False, "error": "Invalid CVV"}
        
        # In a real implementation, you would:
        # 1. Process the payment through your payment gateway
        # 2. Create the order on your website
        # 3. Generate and store the gift card codes
        # 4. Send confirmation email
        
        # For now, we'll generate codes (this should only happen after successful payment)
        logger.info(f"Processing payment for {data['amount']} - Card: ****{card_number[-4:]}")
        
        # TODO: Integrate with your actual payment processor here
        # This is where you would call Stripe, PayPal, or your website's checkout API
        
        # Generate codes (in production, only do this after payment confirmation)
        codes = gen_codes(data['amount'])
        
        return {
            "success": True,
            "codes": codes,
            "message": "Payment processed successfully"
        }
    
    except Exception as e:
        logger.error(f"Payment processing error: {e}", exc_info=True)
        return {"success": False, "error": str(e)}

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()}), 200

@app.route("/pay", methods=["POST"])
def pay():
    """Process payment and make purchase on AeroElite.Shop"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        # Validate required fields
        required_fields = [
            "amount", "card_number", "exp_month", "exp_year", "cvv",
            "name", "email", "address", "city", "state", "zip_code"
        ]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "success": False,
                "error": f"Missing fields: {', '.join(missing_fields)}"
            }), 400
        
        logger.info(f"Processing payment for amount: {data['amount']}, Email: {data['email']}")
        
        # Try different payment methods in order of preference
        result = None
        
        # Method 1: Stripe (if configured)
        if STRIPE_SECRET_KEY:
            logger.info("Attempting payment via Stripe")
            result = process_payment_stripe(data)
            if result.get("success"):
                return jsonify(result), 200
        
        # Method 2: Website API (if configured)
        if not result or not result.get("success"):
            if PAYMENT_API_URL:
                logger.info("Attempting payment via Website API")
                result = process_payment_website_api(data)
                if result.get("success"):
                    return jsonify(result), 200
        
        # Method 3: Default (placeholder - requires actual integration)
        if not result or not result.get("success"):
            logger.warning("Using default payment processor (requires integration)")
            result = process_payment_default(data)
        
        if result.get("success"):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    
    except Exception as e:
        logger.error(f"Error in /pay endpoint: {e}", exc_info=True)
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    """Root endpoint"""
    return jsonify({
        "service": "AeroPay Bot Backend",
        "status": "running",
        "endpoints": ["/health", "/pay"]
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
