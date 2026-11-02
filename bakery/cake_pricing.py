"""
Modular Cake Pricing Engine & Customizer Configuration
Twinklebell Confectionaries London

All options, labels, and prices are defined here in a single editable structure.
This ensures prices and options can be easily modified without touching template or 3D code,
and allows strict server-side validation so client-side pricing is never trusted blindly.
"""

# Base prices by shape and weight/size (serving size)
BASE_PRICES = {
    'round': {
        '1kg': {'price': 45.00, 'servings': '8-10 servings', 'label': '1 kg (Standard · 8-10 servings)'},
        '2kg': {'price': 65.00, 'servings': '15-18 servings', 'label': '2 kg (Medium · 15-18 servings)'},
        '3kg': {'price': 90.00, 'servings': '25-30 servings', 'label': '3 kg (Large · 25-30 servings)'},
    },
    'square': {
        '1kg': {'price': 48.00, 'servings': '10-12 servings', 'label': '1 kg (Standard · 10-12 servings)'},
        '2kg': {'price': 70.00, 'servings': '18-22 servings', 'label': '2 kg (Medium · 18-22 servings)'},
        '3kg': {'price': 95.00, 'servings': '28-32 servings', 'label': '3 kg (Large · 28-32 servings)'},
    },
    'heart': {
        '1kg': {'price': 50.00, 'servings': '8-10 servings', 'label': '1 kg (Standard · 8-10 servings)'},
        '2kg': {'price': 75.00, 'servings': '15-18 servings', 'label': '2 kg (Medium · 15-18 servings)'},
        '3kg': {'price': 100.00, 'servings': '25-28 servings', 'label': '3 kg (Large · 25-28 servings)'},
    },
    'rectangle': {
        '1kg': {'price': 52.00, 'servings': '12-14 servings', 'label': '1 kg (Sheet · 12-14 servings)'},
        '2kg': {'price': 75.00, 'servings': '20-25 servings', 'label': '2 kg (Sheet · 20-25 servings)'},
        '3kg': {'price': 105.00, 'servings': '30-35 servings', 'label': '3 kg (Sheet · 30-35 servings)'},
    },
}

# Extra cost per additional tier
TIER_SURCHARGES = {
    1: 0.00,
    2: 25.00,  # 2 Tiers stacking & doweling
    3: 45.00,  # 3 Tiers structural tiering
}

# Sponge flavors per tier
SPONGE_FLAVORS = {
    'vanilla': {'name': 'Madagascan Vanilla', 'surcharge': 0.00, 'color': '#FDF4DC'},
    'chocolate': {'name': 'Belgian Dark Chocolate', 'surcharge': 3.00, 'color': '#3E2723'},
    'red_velvet': {'name': 'Luxury Red Velvet', 'surcharge': 4.00, 'color': '#8B0000'},
    'strawberry': {'name': 'Wild Strawberry Infusion', 'surcharge': 3.00, 'color': '#FFB6C1'},
    'lemon': {'name': 'Sicilian Zesty Lemon', 'surcharge': 2.00, 'color': '#FFF9A6'},
    'butterscotch': {'name': 'Salted Butterscotch', 'surcharge': 3.00, 'color': '#E0A96D'},
    'marble': {'name': 'Vanilla & Chocolate Marble', 'surcharge': 3.00, 'color': '#A1887F'},
}

# Fillings between layers
FILLINGS = {
    'none': {'name': 'None (Just sponge & crumb)', 'surcharge': 0.00, 'color': '#F5F5DC'},
    'cream': {'name': 'Vanilla Chantilly Cream', 'surcharge': 0.00, 'color': '#FFFDD0'},
    'chocolate_ganache': {'name': 'Whipped Chocolate Ganache', 'surcharge': 3.50, 'color': '#4A2E18'},
    'strawberry_jam': {'name': 'Artisan Strawberry Preserve', 'surcharge': 2.50, 'color': '#C2185B'},
    'caramel': {'name': 'Rich Salted Dulce de Leche', 'surcharge': 3.50, 'color': '#C68B59'},
}

# Frosting types
FROSTING_TYPES = {
    'buttercream': {'name': 'Swiss Meringue Buttercream', 'surcharge': 0.00},
    'whipped_cream': {'name': 'Light Whipped Cream', 'surcharge': 0.00},
    'fondant': {'name': 'Silky Fondant Icing (Smooth)', 'surcharge': 6.00},
    'chocolate_ganache': {'name': 'Velvety Dark Ganache', 'surcharge': 5.00},
    'naked': {'name': 'Semi-Naked (Rustic exposed sponge)', 'surcharge': 0.00},
}

# Preset frosting colors
PRESET_COLORS = [
    {'name': 'Classic Ivory Cream', 'hex': '#FFF8F0'},
    {'name': 'Blush Rose Pink', 'hex': '#F8C8DC'},
    {'name': 'Pastel Baby Blue', 'hex': '#B0E0E6'},
    {'name': 'Sage Olive Green', 'hex': '#C2D4AB'},
    {'name': 'Buttercup Yellow', 'hex': '#FFF3B0'},
    {'name': 'Lilac Lavender', 'hex': '#E6E6FA'},
    {'name': 'Midnight Navy', 'hex': '#1B263B'},
    {'name': 'Deep Chocolate', 'hex': '#4A2E18'},
    {'name': 'Pure Snow White', 'hex': '#FFFFFF'},
    {'name': 'Champagne Gold', 'hex': '#F4E8C1'},
]

# Edge & Finish styles
FINISH_STYLES = {
    'smooth': {'name': 'Smooth Classic Finish', 'surcharge': 0.00},
    'spatula': {'name': 'Artisan Spatula Swirls', 'surcharge': 2.50},
    'swirl': {'name': 'Rosette & Shell Piping', 'surcharge': 3.00},
    'textured': {'name': 'Artisan Textured Palette Knife', 'surcharge': 3.00},
    'drip': {'name': 'Gourmet Drip Cascade', 'surcharge': 4.50},
}

# Drip flavors / colors
DRIP_OPTIONS = {
    'chocolate': {'name': 'Dark Chocolate Drip', 'color': '#3A1E11'},
    'caramel': {'name': 'Golden Salted Caramel Drip', 'color': '#C4823F'},
    'white_chocolate': {'name': 'White Chocolate Silk Drip', 'color': '#FFFBEA'},
    'pink_ruby': {'name': 'Ruby Rose Berry Drip', 'color': '#E06277'},
}

# Toppings & Decorations
TOPPINGS = {
    'strawberries': {'name': 'Fresh British Strawberries', 'surcharge': 3.50, 'type': 'fruit'},
    'cherries': {'name': 'Glossy Maraschino Cherries', 'surcharge': 3.00, 'type': 'fruit'},
    'blueberries': {'name': 'Fresh Wild Blueberries', 'surcharge': 3.00, 'type': 'fruit'},
    'sprinkles': {'name': 'Celebration Confetti Sprinkles', 'surcharge': 1.50, 'type': 'sprinkle'},
    'chocolate_chips': {'name': 'Belgian Chocolate Chips', 'surcharge': 2.00, 'type': 'chocolate'},
    'cookies': {'name': 'Crushed Oreo Cookie Biscuits', 'surcharge': 2.50, 'type': 'cookie'},
    'macarons': {'name': 'Handmade French Macarons (3x)', 'surcharge': 5.00, 'type': 'luxury'},
    'roses': {'name': 'English Garden Rose Petals', 'surcharge': 4.50, 'type': 'luxury'},
    'chocolate_sails': {'name': 'Sculpted Chocolate Wave Sails', 'surcharge': 4.00, 'type': 'luxury'},
    'edible_flowers': {'name': 'Pressed Edible Floral Petals', 'surcharge': 4.00, 'type': 'luxury'},
    'gold_leaf': {'name': '24K Edible Gold Leaf Accents', 'surcharge': 4.50, 'type': 'luxury'},
    'shimmer_spheres': {'name': 'Decorative Shimmering Balloon Spheres', 'surcharge': 4.00, 'type': 'luxury'},
    'candles': {'name': 'Golden Birthday Candles (Pack)', 'surcharge': 2.00, 'type': 'accessory'},
    'pearls': {'name': 'Shimmering Sugar Pearls', 'surcharge': 2.00, 'type': 'sprinkle'},
}

# Stand Styles (Display Pedestal)
STAND_STYLES = [
    {'id': 'porcelain', 'name': 'Porcelain White Pedestal Stand', 'surcharge': 0.00},
    {'id': 'gold_pedestal', 'name': 'Royal Gold Pedestal Stand', 'surcharge': 3.50},
    {'id': 'flat_board', 'name': 'Flat Cake Board Only', 'surcharge': 0.00},
]

# Topping Placement Arrangements
TOPPING_ARRANGEMENTS = [
    {'id': 'crescent', 'name': 'Artisan Crescent (Half-Moon Side)'},
    {'id': 'full_crown', 'name': 'Complete Perimeter Crown'},
    {'id': 'cascade', 'name': 'Cascading Side Waterfall'},
    {'id': 'scattered', 'name': 'Scattered Luxury'},
]

# Fonts for inscription
FONT_STYLES = {
    'elegant': {'name': 'Elegant Script (Calligraphy)', 'css': 'Great Vibes, cursive'},
    'serif': {'name': 'Royal Serif (Classic)', 'css': 'Playfair Display, serif'},
    'modern': {'name': 'Clean Sans (Modern Minimalist)', 'css': 'Nunito, sans-serif'},
    'playful': {'name': 'Playful Fun (Casual Bubbly)', 'css': 'Fredoka, sans-serif'},
}

# Text positions
TEXT_POSITIONS = {
    'top': {'name': 'Top of Cake'},
    'front': {'name': 'Front Side of Cake'},
    'plaque': {'name': 'On White Chocolate Plaque'},
}

# Board colors
BOARD_COLORS = [
    {'name': 'Silver Metallic', 'hex': '#D1D5DB'},
    {'name': 'Royal Gold Foil', 'hex': '#E5C07B'},
    {'name': 'Obsidian Black', 'hex': '#1F2937'},
    {'name': 'Natural Marble White', 'hex': '#F3F4F6'},
]

# Cake Toppers
TOPPERS = {
    'none': {'name': 'No Cake Topper', 'surcharge': 0.00},
    'happy_birthday_gold': {'name': 'Acrylic "Happy Birthday" (Mirror Gold)', 'surcharge': 4.50},
    'happy_birthday_rose': {'name': 'Acrylic "Happy Birthday" (Rose Gold)', 'surcharge': 4.50},
    'celebration_stars': {'name': 'Sparkling Golden Star Burst', 'surcharge': 3.50},
    'congratulations_gold': {'name': 'Acrylic "Congratulations" (Mirror Gold)', 'surcharge': 4.50},
    'milestone_age_gold': {'name': 'Custom Numeric Age Topper (Mirror Gold)', 'surcharge': 4.00},
}

# Occasions
OCCASIONS = [
    {'id': 'birthday', 'name': 'Birthday Party', 'icon': 'fa-cake-candles'},
    {'id': 'wedding', 'name': 'Wedding & Reception', 'icon': 'fa-rings-wedding'},
    {'id': 'anniversary', 'name': 'Anniversary Celebration', 'icon': 'fa-heart'},
    {'id': 'baby_shower', 'name': 'Baby Shower & Reveal', 'icon': 'fa-baby'},
    {'id': 'graduation', 'name': 'Graduation Milestone', 'icon': 'fa-graduation-cap'},
    {'id': 'celebration', 'name': 'General Celebration', 'icon': 'fa-champagne-glasses'},
]


def calculate_custom_cake_price(config):
    """
    Strict server-side price calculator.
    Validates every option and returns (total_price, breakdown_dict).
    Never trusts client prices!
    """
    breakdown = []
    total = 0.0

    # 1. Shape & Weight
    shape = config.get('shape', 'round').lower()
    if shape not in BASE_PRICES:
        shape = 'round'
    
    weight = config.get('weight', '1kg').lower()
    if weight not in BASE_PRICES[shape]:
        weight = '1kg'

    base_data = BASE_PRICES[shape][weight]
    base_price = base_data['price']
    total += base_price
    breakdown.append({
        'item': f"Base Cake ({shape.title()}, {base_data['label']})",
        'cost': base_price
    })

    # 2. Tiers
    tiers = int(config.get('tiers', 1))
    if tiers not in TIER_SURCHARGES:
        tiers = 1
    tier_surcharge = TIER_SURCHARGES.get(tiers, 0.0)
    if tier_surcharge > 0:
        total += tier_surcharge
        breakdown.append({
            'item': f"{tiers}-Tier Stacking & Structure",
            'cost': tier_surcharge
        })

    # 3. Sponge Flavors (per tier)
    tier_flavors = config.get('tier_flavors', {})
    for t_idx in range(1, tiers + 1):
        flv_key = tier_flavors.get(str(t_idx)) or config.get('sponge_flavor', 'vanilla')
        if flv_key in SPONGE_FLAVORS:
            flv_cost = SPONGE_FLAVORS[flv_key]['surcharge']
            if flv_cost > 0:
                total += flv_cost
                breakdown.append({
                    'item': f"Tier {t_idx} Flavor: {SPONGE_FLAVORS[flv_key]['name']}",
                    'cost': flv_cost
                })

    # 4. Filling
    filling_key = config.get('filling', 'cream')
    if filling_key in FILLINGS and FILLINGS[filling_key]['surcharge'] > 0:
        fill_cost = FILLINGS[filling_key]['surcharge']
        total += fill_cost
        breakdown.append({
            'item': f"Layer Filling: {FILLINGS[filling_key]['name']}",
            'cost': fill_cost
        })

    # 5. Frosting Type
    frosting_type = config.get('frosting_type', 'buttercream')
    if frosting_type in FROSTING_TYPES and FROSTING_TYPES[frosting_type]['surcharge'] > 0:
        frost_cost = FROSTING_TYPES[frosting_type]['surcharge']
        total += frost_cost
        breakdown.append({
            'item': f"Frosting: {FROSTING_TYPES[frosting_type]['name']}",
            'cost': frost_cost
        })

    # 6. Finish / Drip
    finish_style = config.get('finish_style', 'smooth')
    if finish_style in FINISH_STYLES and FINISH_STYLES[finish_style]['surcharge'] > 0:
        fin_cost = FINISH_STYLES[finish_style]['surcharge']
        total += fin_cost
        breakdown.append({
            'item': f"Finish: {FINISH_STYLES[finish_style]['name']}",
            'cost': fin_cost
        })

    # 7. Toppings
    selected_toppings = config.get('toppings', [])
    if isinstance(selected_toppings, list):
        for top_key in selected_toppings:
            if top_key in TOPPINGS:
                top_cost = TOPPINGS[top_key]['surcharge']
                total += top_cost
                breakdown.append({
                    'item': f"Topping: {TOPPINGS[top_key]['name']}",
                    'cost': top_cost
                })

    # 8. Topper
    topper_key = config.get('topper', 'none')
    if topper_key in TOPPERS and TOPPERS[topper_key]['surcharge'] > 0:
        topper_cost = TOPPERS[topper_key]['surcharge']
        total += topper_cost
        breakdown.append({
            'item': f"Topper: {TOPPERS[topper_key]['name']}",
            'cost': topper_cost
        })

    # 9. Eggless recipe optional
    if config.get('is_eggless') or config.get('eggless'):
        total += 4.00
        breakdown.append({
            'item': "100% Eggless Artisan Recipe",
            'cost': 4.00
        })

    # 10. Display Stand (Pedestal)
    stand_key = config.get('stand_style', 'porcelain')
    for stand in STAND_STYLES:
        if stand['id'] == stand_key and stand.get('surcharge', 0) > 0:
            s_cost = stand['surcharge']
            total += s_cost
            breakdown.append({
                'item': f"Display: {stand['name']}",
                'cost': s_cost
            })

    return round(total, 2), breakdown


def get_full_catalog_context():
    """
    Returns clean dictionary of all options to pass into templates and client JS.
    """
    return {
        'base_prices': BASE_PRICES,
        'tier_surcharges': TIER_SURCHARGES,
        'sponge_flavors': SPONGE_FLAVORS,
        'fillings': FILLINGS,
        'frosting_types': FROSTING_TYPES,
        'preset_colors': PRESET_COLORS,
        'finish_styles': FINISH_STYLES,
        'drip_options': DRIP_OPTIONS,
        'toppings': TOPPINGS,
        'font_styles': FONT_STYLES,
        'text_positions': TEXT_POSITIONS,
        'board_colors': BOARD_COLORS,
        'toppers': TOPPERS,
        'occasions': OCCASIONS,
        'stand_styles': STAND_STYLES,
        'topping_arrangements': TOPPING_ARRANGEMENTS,
    }
