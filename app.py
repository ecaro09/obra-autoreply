from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)

PAGE_TOKEN   = os.environ.get("PAGE_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "OBRA2026")
PAGE_ID      = "291919391185010"

# ─── REPLIES (original intact + new ones added) ───────────────────────────────
REPLIES = {
"welcome": "Hi {name}! 👋 Salamat sa pag-message sa OBRA Office Furniture!\n\n🏆 10+ Years Trusted | ✅ FREE Installation | 🚚 Nationwide Delivery | 🛡️ 1-Year Warranty\n\nAnong office furniture ang kailangan mo?\nI-type ang tanong mo o pumili:\n\n💰 PRICE - magkano?\n🛒 ORDER - paano mag-order?\n🚚 DELIVERY - libre ba?\n💥 DISCOUNT - may promo?\n🏢 PRODUCTS - anong available?\n\n📖 Catalog: https://tinyurl.com/obra-brochure-updated",

"price": "Hi! 😊 Ito ang aming PINAKA-MABENTA:\n\n🪑 CHAIRS\n• Executive Chair — ₱9,160\n• High Back Mesh (1-yr warranty) — ₱3,630–₱3,900\n• Mid Back Chair — ₱3,765–₱4,275\n• Visitors Chair — ₱2,575\n\n🖥️ TABLES\n• Executive Table Set 1.6m — ₱19,795\n• Executive Table Set 1.8m — ₱20,655\n• L-Type Table — ₱21,065–₱35,565\n• Table Only 1.6m — ₱11,210\n\n🗄️ STEEL STORAGE\n• Steel Cabinet — ₱4,300–₱4,700\n• Glass Cabinet — ₱4,300–₱4,850\n• Filing Cabinet — ₱4,300+\n• Mobile Drawer — ₱3,500–₱3,700\n\n💥 NEGOTIABLE — mas mura pa sa bulk!\n📖 https://tinyurl.com/obra-brochure-updated\n\nAnong items at ilan? Para exact quote! 😊",

"order": "🛒 PAANO MAG-ORDER? (4 Steps lang!)\n\nSTEP 1️⃣ PUMILI\n📖 https://tinyurl.com/obra-brochure-updated\n\nSTEP 2️⃣ IPADALA:\n▪️ Item + Qty\n▪️ Delivery address\n▪️ Contact number\n\nSTEP 3️⃣ KUMUHA NG QUOTE\n✅ Exact price | ✅ Delivery fee | ✅ Lead time\n\nSTEP 4️⃣ BAYAD & DELIVERY!\n🔶 GCash: 0968-887-8850 (Annaliza V)\n🏦 UnionBank: 000690021288 (OBRA-EGC)\n💵 COD available\n✅ FREE Installation!\n\nAnong items ang kailangan? 😊",

"delivery": "🚚 DELIVERY INFO\n\n✅ NATIONWIDE DELIVERY — LUZON, VISAYAS, MINDANAO!\n\n🏙️ NCR/Metro Manila: 1–2 days | FREE installation!\n🌏 Luzon (probinsya): 3–5 days | via trucking/cargo\n🌊 Visayas: 7–10 days | via cargo\n🌴 Mindanao: 10–14 days | via cargo\n\n⚠️ SHOWROOM: Quezon City lang po kami.\nWala kaming branch sa Davao o ibang lugar.\nPero nag-de-deliver kami nationwide! 📦\n\n💰 Libre ang installation sa NCR!\nIpadala ang delivery address at i-compute namin ang fee. 😊\n📞 0915-743-9188",

"discount": "💥 DISCOUNTS & PROMOS SA OBRA!\n\n💸 BULK ORDER — mas marami = mas malaking bawas!\n🏢 COMPANY/B2B — special rate + OR/Invoice\n📦 PACKAGE DEAL — Table+Chair+Cabinet = mas mura!\n🤝 LAHAT NEGOTIABLE — sabihin ang budget!\n\nPara sa pinaka-mababang presyo:\n1️⃣ Items + quantity\n2️⃣ Budget range (optional)\n3️⃣ Bibigyan namin ng BEST DEAL! 💪\n\n📖 https://tinyurl.com/obra-brochure-updated",

"products": "🏢 ANO ANG AMING PRODUCTS?\n\n🪑 CHAIRS: Executive, High Back, Mid Back, Mesh, Visitors, Conference\n🖥️ TABLES: Executive Set, L-Type, Conference, Workstation, Table Only\n🗄️ STORAGE: Steel Cabinet, Glass Cabinet, Filing Cabinet, Locker, Rack, Mobile Drawer\n🏢 SYSTEMS: Modular Workstation, Partition, Custom Furniture\n\n✅ FREE Installation | 🚚 Nationwide | 🛡️ 1-Year Warranty\n💥 Retail & Wholesale!\n\n📖 https://tinyurl.com/obra-brochure-updated\n\nAnong items ang kailangan? 😊",

"chairs": "🪑 OBRA OFFICE CHAIRS:\n\n• Executive Chair (leather) — ₱9,160\n• High Back Mesh (1-yr warranty) — ₱3,630–₱3,900\n• High Back Leather/Fabric — ₱3,765–₱4,275\n• Mid Back Mesh — ₱4,070\n• Visitors Chair (sled type) — ₱2,575\n• Conference Chair — ask price\n\n✅ 1-Year Warranty | 💥 Bulk discount!\nIlang pcs? Para exact quote! 😊",

"tables": "🖥️ OBRA OFFICE TABLES:\n\n• Executive Table Set 1.6m — ₱19,795\n• Executive Table Set 1.8m — ₱20,655\n• L-Type Table — ₱21,065–₱35,565\n• Table Only 1.6m — ₱11,210\n• Table Only 1.8m — ₱12,550\n• Conference Table — ask price\n• Workstation — ask price\n\nColors: brown/oak | Left/Right drawer\n✅ FREE Installation | 💥 Negotiable!\nIlang pcs at anong size? 😊",

"cabinets": "🗄️ OBRA STEEL STORAGE:\n\n• Sliding Steel Cabinet H900 — ₱4,300–₱4,700\n• Glass Cabinet H900 — ₱4,300\n• Glass Cabinet H1060 (3 layers) — ₱4,300–₱4,850\n• Filing Cabinet — ₱4,300+\n• Steel Locker — ask price\n• Steel Rack/Shelving — ask price\n• Mobile Drawer — ₱3,500–₱3,700\n• Extra shelves: +₱500\n\nGauge 20 | Heavy duty | 1-Year Warranty!\nIlang pcs at anong type? 😊",

"location": "📍 OBRA OFFICE FURNITURE\n\n🏢 SHOWROOMS (Quezon City ONLY):\n• Judge Juan Luna, Roosevelt, QC\n  Mon–Fri 9AM–5PM | Sat 9AM–2:30PM\n• 12 Santan, Bagbag, QC 1116\n⚠️ By appointment — call 1 day ahead!\n\n🚚 WALA KAMING BRANCH SA DAVAO O IBANG PROBINSYA.\nPero nag-de-deliver kami NATIONWIDE!\n• Visayas: 7–10 days via cargo\n• Mindanao: 10–14 days via cargo\n• Luzon (probinsya): 3–5 days\n\n📞 0915-743-9188 (Call/Viber)\n📧 obrafurniture@gmail.com\n🌐 www.obrafurniture.com",

"payment": "💳 PAYMENT OPTIONS SA OBRA:\n\n🔶 GCash: 0968-887-8850 (Annaliza V)\n🏦 UnionBank: 000690021288 (OBRA-EGC FURNITURE TRADING)\n💵 Cash on Delivery (COD)\n💵 Cash / Online Banking / E-wallets\n\n📸 Send proof of payment para mapabilis!\n✅ FREE Installation sa lahat ng orders!",

# ── NEW: Order form (fires when client says sige/order/go na) ─────────────────
"order_form": "Ayos na po! Ready na namin i-process 😊\n\nPara ma-reserve at ma-schedule ang delivery, paki-send po ito:\n\n▪️ Name:\n▪️ Complete Address:\n▪️ Contact Number:\n▪️ Company (kung applicable):\n▪️ Landmark:\n\n📦 Kami na bahala sa delivery at FREE installation! ✅\n💳 Payment: GCash 0968-887-8850 | UnionBank 000690021288 | COD",

# ── NEW: Lockers specific (from Melanie ₱14,899 conversion) ──────────────────
"lockers": "🗄️ OBRA LOCKERS:\n\n• 4-door Locker — ask price\n• 6-door Locker — ask price\n• 12-door Locker — ask price\n• 18-door Locker — ₱14,899 per unit\n\nHeavy-duty cold-rolled steel | 1-Year Warranty!\n💥 Bulk order = may discount!\n\nIlang units ang kailangan at ilang doors? Para exact quote! 😊",

# ── NEW: Workstation ──────────────────────────────────────────────────────────
"workstation": "🏢 OBRA WORKSTATIONS & PARTITIONS:\n\n✅ Modular Workstations (2, 4, 6-person)\n✅ Office Partition / Cubicle Systems\n✅ Call Center Setup\n✅ Open Plan Office Furniture\n\n💥 Bulk orders — may special pricing!\n\nIlan po ang staff ninyo? May floor plan ba kayo?\nPara ma-recommend namin ang best layout! 😊",

"default": "Salamat sa pag-message sa OBRA Office Furniture! 😊\n\nI-type ang keyword:\n💰 PRICE — magkano?\n🛒 ORDER — paano mag-order?\n🚚 DELIVERY — libre ba?\n💥 DISCOUNT — may promo?\n🏢 PRODUCTS — anong available?\n🪑 CHAIRS — mga upuan\n🖥️ TABLES — mga mesa\n🗄️ CABINETS — steel storage\n📍 LOCATION — saan kayo?\n💳 PAYMENT — paano magbayad?\n\n📖 https://tinyurl.com/obra-brochure-updated\n📞 0915-743-9188"
}

# ─── KEYWORDS (original + new closing/order keywords from real convos) ─────────
KEYWORDS = {
"price":    ["price","presyo","magkano","how much","quote","halaga","mahal","kantidad","how much is","listed price","quotation","mag quote","tanong presyo"],
"order":    ["order","paano","mag-order","purchase","buy","bibili","bilhin","place order","how to order","pano order","i want","gusto ko","saan bibili"],
"order_form": ["sige po","go na","proceed na","push na","tuloy na","yes po order","confirm","ayos na","ok na po","i-order na","paorder","kukunin ko na","bili na","sige na","oo po","go","agreed","deal","tara na","pursue"],
"delivery": ["delivery","deliver","ship","shipping","padala","libre","free delivery","lalamove","trucking","nationwide","sasakyan","mapadala","mindanao","visayas","luzon","province","region","cargo","forwarder","kelan darating","how long","davao","cebu","iloilo","bohol","palawan","batangas","pampanga","laguna","cavite","bulacan","ilocos","cagayan","zamboanga","cotabato","shipping fee","delivery fee","mapadala sa probinsya","probinsya"],
"discount": ["discount","promo","sale","bawas","mas mura","bulk","wholesale","negotiable","tawad","pwede pa bawasan","may discount","cheaper","mura"],
"products": ["products","ano ang","what do you","meron ba","offer","available","catalog","items","furniture","anong meron","what products","ano po"],
"chairs":   ["chair","upuan","silya","mesh","high back","mid back","executive chair","visitors chair","reclining","office chair","ergonomic","swivel"],
"tables":   ["table","desk","mesa","l-type","executive table","workstation table","conference table","l type","writing table","teachers table","computer table"],
"lockers":  ["locker","18 door","12 door","6 door","4 door","locker cabinet","bagong locker"],
"cabinets": ["cabinet","filing","rack","storage","shelf","shelving","drawer","steel cabinet","estante","file cabinet","steel storage"],
"workstation": ["workstation","partition","cubicle","modular","open plan","divider","office setup","call center","bulk"],
"location": ["location","address","saan","showroom","office","visit","pumunta","store","pickup","nasa saan","where are you","hours","oras","open","bukas","branch","saan kayo","may branch","may showroom","davao branch","cebu branch","provincial branch","meron kayong branch"],
"payment":  ["payment","bayad","gcash","unionbank","cod","cash","bank","bayaran","paano magbayad","payment options","paano bayad","gcash number","account number"],
}

# ─── POSTBACK MAP (ice breakers + menu — now with payloads) ──────────────────
POSTBACK_MAP = {
# Original (keep working)
"GET_STARTED":   "welcome",
"PRICE_QUOTE":   "price",
"VIEW_CATALOG":  "products",
"HOW_TO_ORDER":  "order",
"DELIVERY_INFO": "delivery",
"DISCOUNT_INFO": "discount",
"CHAIRS":        "chairs",
"TABLES":        "tables",
"CABINETS":      "cabinets",
# New ice breaker payloads (just set today)
"PROMOS":        "discount",
"HOW_TO_ORDER":  "order",
"STEEL_CABINETS":"cabinets",
}

def classify(text):
    t = text.lower()
    # Check order_form first (highest priority — closing signal)
    for w in KEYWORDS["order_form"]:
        if w in t:
            return "order_form"
    for intent, words in KEYWORDS.items():
        if intent == "order_form":
            continue
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
                intent  = POSTBACK_MAP.get(payload, "default")
                reply   = REPLIES.get(intent, REPLIES["default"])
                send_msg(psid, reply.replace("{name}",""))
            elif "message" in event:
                msg_data = event["message"]
                if msg_data.get("is_echo"):
                    continue
                # Skip attachments — human verifies payment screenshots
                if msg_data.get("attachments"):
                    continue
                msg = msg_data.get("text","")
                if not msg:
                    continue
                intent = classify(msg)
                reply  = REPLIES.get(intent, REPLIES["default"])
                send_msg(psid, reply.replace("{name}",""))
    return jsonify({"status":"ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
