from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)

PAGE_TOKEN = os.environ.get("PAGE_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "OBRA2026")
PAGE_ID = "291919391185010"

REPLIES = {
"welcome": "Hi {name}! 👋 Salamat sa pag-message sa OBRA Office Furniture!\n\n🏆 10+ Years Trusted | ✅ FREE Installation | 🚚 Nationwide Delivery | 🛡️ 1-Year Warranty\n\nAnong office furniture ang kailangan mo?\nI-type ang tanong mo o pumili:\n\n💰 PRICE - magkano?\n🛒 ORDER - paano mag-order?\n🚚 DELIVERY - libre ba?\n💥 DISCOUNT - may promo?\n🏢 PRODUCTS - anong available?\n\n📖 Catalog: https://tinyurl.com/obra-brochure-updated",

"price": "Hi! 😊 Ito ang aming PINAKA-MABENTA:\n\n🪑 CHAIRS\n• Executive Chair — ₱9,160\n• High Back Mesh (1-yr warranty) — ₱3,630–₱3,900\n• Mid Back Chair — ₱3,765–₱4,275\n• Visitors Chair — ₱2,575\n\n🖥️ TABLES\n• Executive Table Set 1.6m — ₱19,795\n• Executive Table Set 1.8m — ₱20,655\n• L-Type Table — ₱21,065–₱35,565\n• Table Only 1.6m — ₱11,210\n\n🗄️ STEEL STORAGE\n• Steel Cabinet — ₱4,300–₱4,700\n• Glass Cabinet — ₱4,300–₱4,850\n• Filing Cabinet — ₱4,300+\n• Mobile Drawer — ₱3,500–₱3,700\n\n💥 NEGOTIABLE — mas mura pa sa bulk!\n📖 https://tinyurl.com/obra-brochure-updated\n\nAnong items at ilan? Para exact quote! 😊",

"order": "🛒 PAANO MAG-ORDER? (4 Steps lang!)\n\nSTEP 1️⃣ PUMILI\n📖 https://tinyurl.com/obra-brochure-updated\n\nSTEP 2️⃣ IPADALA:\n▪️ Item + Qty\n▪️ Delivery address\n▪️ Contact number\n\nSTEP 3️⃣ KUMUHA NG QUOTE\n✅ Exact price | ✅ Delivery fee | ✅ Lead time\n\nSTEP 4️⃣ BAYAD & DELIVERY!\n🔶 GCash: 0968-887-8850 (Annaliza V)\n🏦 UnionBank: 000690021288 (OBRA-EGC)\n💵 COD available\n✅ FREE Installation!\n\nAnong items ang kailangan? 😊",

"delivery": "🚚 DELIVERY & SHIPPING INFO\n\n✅ FREE INSTALLATION — LAHAT NG ITEMS!\n\n🏙️ Metro Manila — Lalamove (1–2 days)\n🌏 Nationwide — Trucking (2–5 days)\n🌊 Islands — Logistics partner available\n🚌 Bus Liner Drop & Go — available\n\n💰 May FREE delivery promo sa selected areas!\nIpadala ang address para ma-check! 😊\n\n📍 Pick-up: Judge Juan Luna, Roosevelt, QC\n📞 0915-743-9188",

"discount": "💥 DISCOUNTS & PROMOS SA OBRA!\n\n💸 BULK ORDER — mas marami = mas malaking bawas!\n🏢 COMPANY/B2B — special rate + OR/Invoice\n📦 PACKAGE DEAL — Table+Chair+Cabinet = mas mura!\n🤝 LAHAT NEGOTIABLE — sabihin ang budget!\n\nPara sa pinaka-mababang presyo:\n1️⃣ Items + quantity\n2️⃣ Budget range (optional)\n3️⃣ Bibigyan namin ng BEST DEAL! 💪\n\n📖 https://tinyurl.com/obra-brochure-updated",

"products": "🏢 ANO ANG AMING PRODUCTS?\n\n🪑 CHAIRS: Executive, High Back, Mid Back, Mesh, Visitors, Conference\n🖥️ TABLES: Executive Set, L-Type, Conference, Workstation, Table Only\n🗄️ STORAGE: Steel Cabinet, Glass Cabinet, Filing Cabinet, Locker, Rack, Mobile Drawer\n🏢 SYSTEMS: Modular Workstation, Partition, Custom Furniture\n\n✅ FREE Installation | 🚚 Nationwide | 🛡️ 1-Year Warranty\n💥 Retail & Wholesale!\n\n📖 https://tinyurl.com/obra-brochure-updated\n\nAnong items ang kailangan? 😊",

"chairs": "🪑 OBRA OFFICE CHAIRS:\n\n• Executive Chair (leather) — ₱9,160\n• High Back Mesh (1-yr warranty) — ₱3,630–₱3,900\n• High Back Leather/Fabric — ₱3,765–₱4,275\n• Mid Back Mesh — ₱4,070\n• Visitors Chair (sled type) — ₱2,575\n• Conference Chair — ask price\n\n✅ 1-Year Warranty | 💥 Bulk discount!\nIlang pcs? Para exact quote! 😊",

"tables": "🖥️ OBRA OFFICE TABLES:\n\n• Executive Table Set 1.6m — ₱19,795\n• Executive Table Set 1.8m — ₱20,655\n• L-Type Table — ₱21,065–₱35,565\n• Table Only 1.6m — ₱11,210\n• Table Only 1.8m — ₱12,550\n• Conference Table — ask price\n• Workstation — ask price\n\nColors: brown/oak | Left/Right drawer\n✅ FREE Installation | 💥 Negotiable!\nIlang pcs at anong size? 😊",

"cabinets": "🗄️ OBRA STEEL STORAGE:\n\n• Sliding Steel Cabinet H900 — ₱4,300–₱4,700\n• Glass Cabinet H900 — ₱4,300\n• Glass Cabinet H1060 (3 layers) — ₱4,300–₱4,850\n• Filing Cabinet — ₱4,300+\n• Steel Locker — ask price\n• Steel Rack/Shelving — ask price\n• Mobile Drawer — ₱3,500–₱3,700\n• Extra shelves: +₱500\n\nGauge 20 | Heavy duty | 1-Year Warranty!\nIlang pcs at anong type? 😊",

"location": "📍 OBRA OFFICE FURNITURE\n\nSHOWROOM:\nJudge Juan Luna, Roosevelt, Quezon City\n🕐 Mon–Fri: 9AM–5PM | Sat: 9AM–2:30PM\n⚠️ By appointment — call 1 day ahead!\n\nSATELLITE OFFICE:\n12 Santan, Bagbag, Quezon City\n\n📞 0915-743-9188 (Call/Viber)\n📧 obrafurniture@gmail.com\n🌐 www.obrafurniture.com",

"payment": "💳 PAYMENT OPTIONS SA OBRA:\n\n🔶 GCash: 0968-887-8850 (Annaliza V)\n🏦 UnionBank: 000690021288 (OBRA-EGC FURNITURE TRADING)\n💵 Cash on Delivery (COD)\n💵 Cash / Online Banking / E-wallets\n\n📸 Send proof of payment para mapabilis!\n✅ FREE Installation sa lahat ng orders!",

"default": "Salamat sa pag-message sa OBRA Office Furniture! 😊\n\nI-type ang keyword:\n💰 PRICE — magkano?\n🛒 ORDER — paano mag-order?\n🚚 DELIVERY — libre ba?\n💥 DISCOUNT — may promo?\n🏢 PRODUCTS — anong available?\n🪑 CHAIRS — mga upuan\n🖥️ TABLES — mga mesa\n🗄️ CABINETS — steel storage\n📍 LOCATION — saan kayo?\n💳 PAYMENT — paano magbayad?\n\n📖 https://tinyurl.com/obra-brochure-updated\n📞 0915-743-9188"
}

KEYWORDS = {
"price": ["price","presyo","magkano","how much","quote","halaga","mahal","kantidad","how much is","listed price"],
"order": ["order","paano","mag-order","purchase","buy","bibili","bilhin","place order","how to order","pano order","i want","gusto ko","saan bibili"],
"delivery": ["delivery","deliver","ship","shipping","padala","libre","free delivery","lalamove","trucking","nationwide","sasakyan","mapadala"],
"discount": ["discount","promo","sale","bawas","mas mura","bulk","wholesale","negotiable","tawad","pwede pa bawasan","may discount"],
"products": ["products","ano ang","what do you","meron ba","offer","available","catalog","items","furniture","anong meron","what products","ano po"],
"chairs": ["chair","upuan","silya","mesh","high back","mid back","executive chair","visitors chair","reclining","office chair"],
"tables": ["table","desk","mesa","l-type","executive table","workstation","conference table","l type","writing table"],
"cabinets": ["cabinet","filing","locker","rack","storage","shelf","shelving","drawer","steel cabinet","estante","cabinet"],
"location": ["location","address","saan","showroom","office","visit","pumunta","store","pickup","nasa saan","where are you"],
"payment": ["payment","bayad","gcash","unionbank","cod","cash","bank","bayaran","paano magbayad","payment options","paano bayad"]
}

POSTBACK_MAP = {
"GET_STARTED":"welcome","PRICE_QUOTE":"price","VIEW_CATALOG":"products",
"HOW_TO_ORDER":"order","DELIVERY_INFO":"delivery","DISCOUNT_INFO":"discount",
"CHAIRS":"chairs","TABLES":"tables","CABINETS":"cabinets"
}

def classify(text):
    t = text.lower()
    for intent, words in KEYWORDS.items():
        if any(w in t for w in words):
            return intent
    return "default"

def send_msg(psid, text):
    try:
        requests.post(
            f"https://graph.facebook.com/v21.0/{PAGE_ID}/messages",
            headers={"Authorization": f"Bearer {PAGE_TOKEN}"},
            json={"recipient":{"id":psid},"message":{"text":text},"messaging_type":"RESPONSE"},
            timeout=10
        )
    except Exception as e:
        print(f"Send error: {e}")

@app.route("/", methods=["GET"])
def home():
    return "✅ OBRA Auto-Reply Bot is Running!"

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid verify token", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status":"ok"})
    for entry in data.get("entry", []):
        for event in entry.get("messaging", []):
            psid = event["sender"]["id"]
            if psid == PAGE_ID:
                continue
            if "postback" in event:
                payload = event["postback"].get("payload","")
                intent = POSTBACK_MAP.get(payload, "default")
                send_msg(psid, REPLIES[intent].replace("{name}",""))
            elif "message" in event:
                msg_data = event["message"]
                if msg_data.get("is_echo"):
                    continue
                msg = msg_data.get("text","")
                if not msg:
                    continue
                intent = classify(msg)
                send_msg(psid, REPLIES[intent].replace("{name}",""))
    return jsonify({"status":"ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
