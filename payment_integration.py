"""
Payment integration skeleton for Iconora Studio
- Supports Gumroad purchase link (simple redirect to product page)
- Provides a skeleton for Stripe checkout session creation (requires Flask and stripe)
- Provides webhook verification guidance

Usage:
- For Gumroad: use direct purchase links (no server required)
- For Stripe: run a small server to create Checkout Sessions and verify webhooks
"""

# Minimal Gumroad helper
def gumroad_product_link(product_slug: str) -> str:
    """Return a Gumroad product purchase URL for the given slug."""
    return f"https://gumroad.com/l/{product_slug}"


# Stripe skeleton (requires `stripe` package)
try:
    import stripe
except Exception:
    stripe = None

STRIPE_SECRET_KEY = "sk_test_YOUR_KEY"
STRIPE_WEBHOOK_SECRET = "whsec_YOUR_SECRET"

def create_stripe_checkout_session(amount_cents: int, currency: str = "usd", success_url: str = "", cancel_url: str = "") -> dict:
    """Create a Stripe Checkout Session. Requires stripe.api_key to be set."""
    if not stripe:
        raise RuntimeError("stripe package not installed")
    stripe.api_key = STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            'price_data': {
                'currency': currency,
                'product_data': {'name': 'Iconora Studio License'},
                'unit_amount': amount_cents,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session


# Webhook verification helper
def verify_stripe_webhook(payload: bytes, sig_header: str) -> dict:
    """Verify Stripe webhook signature and return event dict."""
    if not stripe:
        raise RuntimeError("stripe package not installed")
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        raise
    return event


if __name__ == "__main__":
    print("Payment integration helper: Gumroad & Stripe skeleton")
    print("Example Gumroad Pro link:", gumroad_product_link('iconora-pro'))
