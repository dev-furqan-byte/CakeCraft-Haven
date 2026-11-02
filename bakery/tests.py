import json
import base64
from django.test import TestCase, Client
from django.urls import reverse
from bakery.models import Order, OrderItem
from bakery.cake_pricing import (
    BASE_PRICES,
    TIER_SURCHARGES,
    calculate_custom_cake_price,
    get_full_catalog_context,
)

class CakePricingEngineTests(TestCase):
    """Unit tests for the server-side cake pricing and validation engine"""

    def test_default_round_1kg_pricing(self):
        """A standard 1-tier 1kg round cake with default vanilla sponge and cream filling"""
        config = {
            'shape': 'round',
            'weight': '1kg',
            'tiers': 1,
            'sponge_flavor': 'vanilla',
            'filling': 'cream',
            'frosting_type': 'buttercream',
            'finish_style': 'smooth',
            'toppings': [],
            'topper': 'none',
            'eggless': False
        }
        total, breakdown = calculate_custom_cake_price(config)
        self.assertEqual(total, 45.00)
        self.assertTrue(any("Base Cake" in item['item'] for item in breakdown))

    def test_multi_tier_surcharges(self):
        """2-Tier and 3-Tier structural stacking surcharges"""
        config_2tier = {'shape': 'round', 'weight': '1kg', 'tiers': 2}
        total_2, _ = calculate_custom_cake_price(config_2tier)
        # 45.00 base + 25.00 2-tier surcharge = 70.00
        self.assertEqual(total_2, 70.00)

        config_3tier = {'shape': 'round', 'weight': '1kg', 'tiers': 3}
        total_3, _ = calculate_custom_cake_price(config_3tier)
        # 45.00 base + 45.00 3-tier surcharge = 90.00
        self.assertEqual(total_3, 90.00)

    def test_heart_and_square_shape_pricing(self):
        """Heart and square shapes have their own custom base matrices"""
        config_heart = {'shape': 'heart', 'weight': '2kg', 'tiers': 1}
        total_heart, _ = calculate_custom_cake_price(config_heart)
        self.assertEqual(total_heart, 75.00)

        config_square = {'shape': 'square', 'weight': '3kg', 'tiers': 1}
        total_square, _ = calculate_custom_cake_price(config_square)
        self.assertEqual(total_square, 95.00)

    def test_premium_flavor_and_eggless_surcharges(self):
        """Red velvet sponge, ganache filling, chocolate drip, macarons, and eggless option"""
        config = {
            'shape': 'round',
            'weight': '1kg',
            'tiers': 1,
            'sponge_flavor': 'red_velvet',      # +4.00
            'filling': 'chocolate_ganache',      # +3.50
            'frosting_type': 'fondant',          # +6.00
            'finish_style': 'drip',              # +4.50
            'toppings': ['macarons', 'candles'], # 5.00 + 2.00 = 7.00
            'topper': 'happy_birthday_gold',     # +4.50
            'eggless': True                      # +4.00
        }
        # Base (45) + 4 + 3.5 + 6 + 4.5 + 7 + 4.5 + 4 = 78.50
        total, breakdown = calculate_custom_cake_price(config)
        self.assertEqual(total, 78.50)
        self.assertEqual(len(breakdown), 9)

    def test_invalid_input_fallback_sanitization(self):
        """Ensure malicious or non-existent options fallback safely to defaults"""
        malicious_config = {
            'shape': 'pentagon_injection_attack',
            'weight': '999kg',
            'tiers': 99,
            'sponge_flavor': 'unknown_toxic_flavor',
            'filling': 'undefined_paste',
            'frosting_type': 'hack_frosting',
            'finish_style': 'fake_finish',
            'toppings': ['non_existent_item'],
            'topper': 'hacker_topper',
            'eggless': False
        }
        total, breakdown = calculate_custom_cake_price(malicious_config)
        # Should fallback safely to round 1kg 1-tier (£45.00)
        self.assertEqual(total, 45.00)


class CustomCakeEndpointsTests(TestCase):
    """Integration tests for HTTP endpoints and order generation"""

    def setUp(self):
        self.client = Client()

    def test_make_your_own_cake_page_renders(self):
        """Ensure the /make-your-own-cake/ page loads with HTTP 200 and customizer data"""
        response = self.client.get(reverse('make_your_own_cake'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Make Your Own Cake")
        self.assertContains(response, "3D Studio")

    def test_api_cake_pricing_post(self):
        """Ensure /api/cake-pricing/ returns JSON with accurate price"""
        payload = {
            'shape': 'round',
            'weight': '2kg',
            'tiers': 2,
            'sponge_flavor': 'chocolate',
            'filling': 'caramel'
        }
        response = self.client.post(
            reverse('api_cake_pricing'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success'))
        # Base 65.00 + 2-Tier 25.00 + Chocolate sponge 3.00 * 2 tiers + Caramel 3.50 = 99.50
        self.assertEqual(data.get('total_price'), 99.50)

    def test_order_custom_cake_flow(self):
        """Submit a complete custom 3D cake order and verify database record"""
        dummy_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        cake_config = {
            'shape': 'heart',
            'weight': '1kg',
            'tiers': 1,
            'sponge_flavor': 'red_velvet',
            'filling': 'cream',
            'frosting_color': '#F8C8DC',
            'message_text': 'Happy Birthday Sophia',
            'toppings': ['strawberries'],
            'eggless': False
        }

        form_data = {
            'config': json.dumps(cake_config),
            'snapshot_data': dummy_base64,
            'customer_name': 'Sophia Higgins',
            'customer_email': 'sophia.higgins@example.co.uk',
            'customer_phone': '+44 7700 900077',
            'delivery_address': 'Flat 4B, Kensington High Street, London',
            'preferred_delivery_date': '2026-12-25',
            'special_notes': 'Please deliver before noon.',
            'payment_method': 'COD'
        }

        response = self.client.post(reverse('order_custom_cake'), data=form_data)
        # Should redirect to track_order
        self.assertEqual(response.status_code, 302)

        # Verify Order in DB
        custom_orders = Order.objects.filter(order_type='CUSTOM')
        self.assertEqual(custom_orders.count(), 1)
        order = custom_orders.first()

        self.assertEqual(order.customer_name, 'Sophia Higgins')
        self.assertEqual(order.payment_method, 'COD')
        self.assertEqual(order.cake_message, 'Happy Birthday Sophia')
        # Heart 1kg (50.00) + Red Velvet (4.00) + Strawberries (3.50) = 57.50
        self.assertEqual(float(order.total_amount), 57.50)
        self.assertTrue(bool(order.custom_cake_snapshot))
        self.assertEqual(order.custom_cake_config.get('shape'), 'heart')
