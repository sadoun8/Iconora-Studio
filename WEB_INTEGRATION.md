Website integration instructions (Carrd / Webflow / Static)

1) Add Buy links (Gumroad)
- For simple distribution, create Gumroad products for Pro and Enterprise.
- Use the product slugs in the landing page buttons.
  Example: https://gumroad.com/l/iconora-pro

2) Stripe Checkout (custom site)
- Create a small backend endpoint to create a Checkout Session (see `payment_integration.py`).
- Use Stripe Checkout client to redirect users to the session URL.
- Implement webhook endpoint to fulfill purchase and send license key via email.

3) Embedding on Carrd
- Carrd allows `Buy` buttons that redirect to Gumroad links.
- Add a button element, set the link to the Gumroad product URL.
- For Stripe, you need a server; use the button to call your API which returns a Checkout URL.

4) Webflow
- Add button with external link to Gumroad, or use custom code to call your server for Stripe session.
- Use Webflow Forms to capture email, then redirect to the checkout URL.

5) Sending License Key
- After successful payment, send license key to buyer email automatically.
- For Gumroad: use Gumroad webhooks to trigger a server-side process that issues the deterministic key (based on buyer name/email and edition) and emails the buyer.
- For Stripe: verify webhook `checkout.session.completed` then generate license and email.

6) Security & Anti-Fraud
- Verify webhooks using provider secrets.
- Rate-limit license generation endpoints.
- Store issued licenses in secure storage (encrypted file or DB).

7) Testing
- Test in sandbox mode (Stripe test keys, Gumroad test purchases)
- Validate webhook signatures
- Ensure license delivery and activation flow works offline after initial activation

8) Example flow (Stripe)
- User clicks Buy → front-end calls `/create-checkout-session` → server returns session.url → front-end redirects
- After payment, Stripe sends `checkout.session.completed` webhook → server verifies → server generates license → server emails license to customer
