# Twinklebell Confectionaries — Django & Stripe Full Stack Store

A full-stack e-commerce and artisan bakery operations suite for **Twinklebell Confectionaries** (London, UK), built with Python, Django, Tailwind CSS, Stripe Checkout, and Live Kitchen Cake Tracking.

---

## 🚀 Complete Feature Suite

### 1. Guest Checkout & Advanced Cake Customization (No Login Needed)
- Customers can order and customize any cake without registering:
  - **Cake Size & Servings:** 6" (8-10 Servings), 8" (12-15 Servings), 10" (15-20 Servings), or 2-Tier Celebration.
  - **Quantity:** 1 or multiple cakes.
  - **Sponge Flavour:** Victoria Sponge, Lemon Drizzle, Belgian Chocolate, Spiced Carrot, Red Velvet.
  - **Colour Palette:** Ivory & Gold, Pastel Pink & Rose, Soft Sage & Peach, Baby Blue, Chocolate Ganache.
  - **Cake Inscription:** Custom hand-piped message (e.g. *"Happy 30th Birthday Sarah!"*).
  - **Design / Reference Photo Upload:** Customer can attach inspiration cake pictures.
  - **Customer Contact:** Name, Email (for instant tracking updates), Phone, UK Delivery Address & Postcode, Preferred Date, Allergens.

### 2. "Make Your Own Cake" Interactive 3D Studio (`/make-your-own-cake/`)
- **Game-like Visual Playground:**
  - Customers build their bespoke celebration cake in real time in a 3D browser viewport powered by **Three.js** and OrbitControls (drag to rotate, pinch/scroll to zoom, auto-rotation).
  - Built **100% procedurally from geometry** (cylinders for round tiers, extruded shapes for heart/square/sheet, piping rings, procedural drip mesh, sprinkles and fruits) — zero heavy 3D asset downloads required, running smoothly on mobile and desktop.
  - **Graceful 2D Fallback:** Automatically switches to a clean 2D layered canvas if WebGL is unavailable or fails.
  - **Playground Controls:** "Surprise Me" randomizer, Undo, Redo, Reset, and celebratory confetti upon order completion.
  - **Real-Time 3D Inscription:** Customer types their message (e.g., *"Happy Birthday Ayesha"*), picks font and position (top, front, or chocolate plaque), and it renders live onto the 3D cake canvas.
- **Full Customization Options Matrix:**
  1. *Shape:* Round, Square, Heart, Sheet / Rectangle.
  2. *Tiers & Weight:* 1, 2, or 3 tiers (with doweling structure), 1kg, 2kg, or 3kg serving sizes.
  3. *Sponge Flavors (per tier):* Madagascan Vanilla, Belgian Dark Chocolate, Luxury Red Velvet, Wild Strawberry, Sicilian Lemon, Salted Butterscotch, Marble.
  4. *Fillings:* Chantilly Cream, Whipped Ganache, Strawberry Preserve, Salted Caramel, or None.
  5. *Frosting & Colors:* Swiss Buttercream, Whipped Cream, Fondant, Ganache, Semi-Naked; 10 curated designer palette presets plus full custom hex picker.
  6. *Finishes & Drips:* Smooth, Rosette Piping, Textured Palette, Gourmet Drip (Dark Chocolate, Golden Caramel, White Silk, Ruby Rose).
  7. *Artisan Toppings:* Fresh Strawberries, Cherries, Blueberries, Celebration Confetti, Chocolate Chips, Oreo Pieces, French Macarons, Edible Flowers, Gold Candles, Sugar Pearls.
  8. *Board & Extras:* Silver Metallic, Gold Foil, Obsidian Black, Marble White boards; Acrylic "Happy Birthday" or Star toppers; 100% Eggless recipe toggle.
- **Server-Side Pricing Engine (`bakery/cake_pricing.py`):**
  - Prices update dynamically via `/api/cake-pricing/`.
  - Every order recomputes and validates total price strictly on the server before database persistence — client prices are never trusted.
- **Snapshot Capture & Ordering Flow:**
  - High-res PNG snapshot is rendered from the 3D canvas via `toDataURL` and saved to `media/custom_cakes/`.
  - Complete configuration JSON and snapshot image are stored directly in the `Order` model (`order_type='CUSTOM'`).
  - Seamlessly routes into checkout (Cash on Delivery or Stripe).
- **Admin & Kitchen Operations:**
  - Orders marked with `🎨 3D Custom` badges and filterable with 1-click in `/admin/?type=CUSTOM`.
  - Admin view renders full 3D snapshot (view & download PNG) alongside full human-readable spec sheet.
  - Printable kitchen slip (`/admin/orders/<id>/kitchen-ticket/`) prints the 3D visual photo and pastry chef production matrix.

### 3. Live Order Tracking System (`/track-order/`)
- Every confirmed order generates a unique **Order Tracking ID** (e.g. `TRK-XXXXXX`).
- Customer can paste their Tracking ID into the website's search bar anytime to view:
  - **Overall Progress Percentage Bar** (e.g. 65% Complete).
  - **8-Stage Live Kitchen Stepper:**
    1. Order Confirmed & Paid
    2. Batter Mixing
    3. Freshly Baking in the Oven
    4. Cooling & Sponge Layering
    5. Buttercream & Custom Hand-Piping
    6. Quality Inspection & Packaging
    7. Dispatched / Out for Delivery
    8. Successfully Delivered
  - **Live Baker's Update Notes** (e.g. *"Sponge has cooled, now piping custom message"*).
  - **Estimated Delivery Schedule / Time Remaining**.
  - **Live Kitchen Activity Log / Timeline:** Historical record of every baking stage milestone with timestamps!
  - Full customized cake specifications & uploaded reference photo preview.

### 3. Executive Heavy Bakery Admin Dashboard (`/admin/`)
- **Direct Access at `/admin/`:** Clean staff login redirects straight into the Executive Dashboard.
- **Visual Analytics with Chart.js:**
  - Kitchen Stage Pipeline Donut Chart (Oven vs Piping vs Prep vs Dispatched).
  - Order Status Breakdown Bar Chart.
- **KPI Summary Cards:** Gross Revenue (£ GBP), Total Orders, Paid Orders, In Kitchen, Dispatched, Delivered.
- **Real-Time Kitchen Progress Editor:**
  - Update baking stage (1 to 8).
  - Update progress percentage (0-100%).
  - Update estimated time left.
  - Write live baker notes that update the customer's tracking page immediately!
- **Printable Chef Production Docket / Kitchen Slip:**
  - 1-click printable receipt designed for baking benches and cake box labels.
  - Includes prominent hand-piping inscription, dietary/allergy warnings, and chef checklists.
- **1-Click WhatsApp Customer Update:**
  - Instantly generates a customized WhatsApp update message for the customer with their tracking link and current baking stage!
- **Excel / CSV Order Export:**
  - 1-click download of all customer orders, delivery addresses, and revenue for accounting.
- **Direct Add New Cake to Menu Modal:**
  - Create new cake products directly from the dashboard without navigating away.
- **Filter & Search:** Filter by status (Paid, Processing, Dispatched, Delivered) or search by ID, name, email.

### 4. Automated Dual Email System (Gmail SMTP)
- **Instant Dispatch:** As soon as customer submits the order, notifications are fired immediately!
- **Customer Email:** Sends order receipt + **Order Tracking ID** + clickable direct tracking link.
- **Admin Email (`furqanhameed55667788@gmail.com`):** Real-time alert with all customer details, cake customization, and tracking ID.

### 5. Stripe Payment Gateway
- Real-time Stripe Checkout in GBP (£).
- Supports test card numbers in Test Mode.
- Webhook & Payment Success callback to automate order fulfillment.

---

## 🛠️ How to Run the Project

### 1. Start the Django Server
```bash
python manage.py runserver
```
Open your browser and navigate to:
👉 **http://localhost:8000/**

### 2. Live Order Tracking (Customer View)
👉 **http://localhost:8000/track-order/**
- Paste any Tracking ID (e.g. `TRK-D64177`) to see the live 8-stage interactive stepper and kitchen activity log.

### 3. Executive Heavy Bakery Admin Dashboard
👉 **http://localhost:8000/admin/**
- **Username:** `admin`
- **Password:** `admin12345`

### 4. Standard Django Database Admin (Optional)
👉 **http://localhost:8000/django-admin/**
- **Username:** `admin`
- **Password:** `admin12345`

---

## 🎂 How to Edit Custom Cake Options & Pricing

All options, flavors, colors, toppings, and price surcharges are centralized in a single Python file:
📁 **`bakery/cake_pricing.py`**

### Modifying Base Prices
```python
BASE_PRICES = {
    'round': {
        '1kg': {'price': 45.00, 'servings': '8-10 servings', 'label': '1 kg (Standard · 8-10 servings)'},
        '2kg': {'price': 65.00, 'servings': '15-18 servings', 'label': '2 kg (Medium · 15-18 servings)'},
        '3kg': {'price': 90.00, 'servings': '25-30 servings', 'label': '3 kg (Large · 25-30 servings)'},
    },
    # square, heart, rectangle...
}
```

### Adding New Toppings or Flavors
To add a new topping, simply add an entry to the `TOPPINGS` dictionary in `bakery/cake_pricing.py`:
```python
TOPPINGS['gold_flakes'] = {
    'name': '24k Edible Gold Leaf',
    'surcharge': 6.50,
    'type': 'luxury'
}
```
The frontend options catalog and the server pricing validation engine will pick it up automatically without needing template or database changes!

---

## 🧪 Running Automated Unit Tests
To verify the pricing engine and custom order flow:
```bash
python manage.py test bakery
```

# CakeCraft-Haven
A complete online bakery store built with Django, featuring cake and bakery product browsing, online ordering, secure Stripe payments, order management, and an interactive 3D cake customization studio with real-time previews and dynamic pricing.
