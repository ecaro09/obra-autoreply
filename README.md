# OBRA Office Furniture — Auto-Reply Bot

Facebook Messenger auto-reply webhook for OBRA Office Furniture page.

## Setup

### Environment Variables (set in Render/Railway)
- `PAGE_TOKEN` = your Facebook Page Access Token
- `VERIFY_TOKEN` = OBRA2026

### Deploy on Render.com
1. Connect this GitHub repo to Render
2. New Web Service → select this repo
3. Build: `pip install -r requirements.txt`
4. Start: `gunicorn app:app`
5. Add env vars above

### Connect to Facebook
1. Go to developers.facebook.com → your app
2. Messenger → Webhooks → Edit
3. Callback URL: https://your-render-url.onrender.com/webhook
4. Verify Token: OBRA2026
5. Subscribe to: messages, messaging_postbacks

## Keywords Handled
- PRICE / PRESYO / MAGKANO
- ORDER / PAANO MAG-ORDER
- DELIVERY / PADALA / LIBRE
- DISCOUNT / PROMO / TAWAD
- PRODUCTS / ANO ANG MERON
- CHAIRS / UPUAN / SILYA
- TABLES / MESA / DESK
- CABINETS / FILING / LOCKER
- LOCATION / SAAN / SHOWROOM
- PAYMENT / BAYAD / GCASH
