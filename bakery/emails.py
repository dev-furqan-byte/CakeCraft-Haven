import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)

def send_order_emails(order, request=None):
    """
    Sends refined, minimalist, professional HTML order notifications
    to Admin and Customer. Designed with an editorial, premium British
    patisserie aesthetic without AI clutter or flashy emojis.
    """
    domain = "http://127.0.0.1:8000"
    if request:
        scheme = 'https' if request.is_secure() else 'http'
        domain = f"{scheme}://{request.get_host()}"

    track_url = f"{domain}/track-order/?tracking_id={order.tracking_id}"
    admin_url = f"{domain}/admin/"

    snapshot_url = f"{domain}{order.custom_cake_snapshot.url}" if order.custom_cake_snapshot else ""
    is_custom = order.order_type == 'CUSTOM'
    custom_cfg = order.custom_cake_config or {}

    custom_specs_html = ""
    if is_custom and custom_cfg:
        toppings_str = ", ".join(t.replace('_', ' ').title() for t in custom_cfg.get('toppings', [])) or 'None'
        eggless_row = """
              <tr>
                <td style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; color: #047857; font-weight: 600;">Dietary Standard</td>
                <td align="right" style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; color: #047857; font-weight: 600;">100% Pure Eggless Recipe</td>
              </tr>
        """ if custom_cfg.get('eggless') else ""

        custom_specs_html = f"""
              <tr>
                <td style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; color: #696158;">Cake Type</td>
                <td align="right" style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; font-weight: 600; color: #7C3AED;">Custom 3D Procedural Design</td>
              </tr>
              <tr>
                <td style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; color: #696158;">Filling Layer</td>
                <td align="right" style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; font-weight: 600; color: #1E1B18;">{custom_cfg.get('filling', 'cream').replace('_', ' ').title()}</td>
              </tr>
              <tr>
                <td style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; color: #696158;">Toppings &amp; Extras</td>
                <td align="right" style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; color: #1E1B18;">{toppings_str}</td>
              </tr>
              <tr>
                <td style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; color: #696158;">Cake Board &amp; Topper</td>
                <td align="right" style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; color: #1E1B18;">{custom_cfg.get('board_color', 'Silver')} · {custom_cfg.get('topper', 'None').replace('_', ' ').title()}</td>
              </tr>
              {eggless_row}
        """

    snapshot_block_html = f"""
            <div style="margin-bottom: 24px; text-align: center; background-color: #FAFAF8; border: 1px solid #ECE7DF; border-radius: 6px; padding: 16px;">
              <div style="font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; color: #8A8177; font-weight: 600; margin-bottom: 10px;">3D Cake Design Snapshot</div>
              <a href="{snapshot_url}" target="_blank">
                <img src="{snapshot_url}" alt="Custom Cake Design" style="max-width: 100%; height: auto; max-height: 220px; border-radius: 4px; display: inline-block;">
              </a>
            </div>
    """ if snapshot_url else ""

    # ========================================================
    # 1. ADMIN NOTIFICATION EMAIL
    # ========================================================
    try:
        admin_email = getattr(settings, 'ADMIN_NOTIFICATION_EMAIL', None)
        if admin_email:
            subject = f"New Order: #{order.order_number} — £{order.total_amount} ({order.customer_name})"
            
            plain_text = f"""NEW ORDER RECEIVED
Order Reference: #{order.order_number}
Tracking Reference: {order.tracking_id}
Customer: {order.customer_name} ({order.customer_email})
Phone: {order.customer_phone or 'Not provided'}
Total: £{order.total_amount} GBP

Specifications:
- Size: {order.cake_size}
- Flavour: {order.cake_flavour}
- Palette: {order.cake_colour}
- Inscription: {order.cake_message or 'None'}
- Dietary Notes: {order.dietary_notes or 'None'}
- Preferred Delivery: {order.preferred_delivery_date or 'Standard delivery schedule'}
- Address: {order.delivery_address or 'Standard UK Delivery'}

Kitchen Dashboard: {admin_url}
Customer Tracker: {track_url}
"""

            admin_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>New Order #{order.order_number}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #F6F4F0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; color: #1E1B18; -webkit-font-smoothing: antialiased;">
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #F6F4F0; padding: 36px 12px;">
  <tr>
    <td align="center">
      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 560px; background-color: #FFFFFF; border: 1px solid #E6E1DA; border-radius: 8px; overflow: hidden;">
        
        <!-- Brand Header -->
        <tr>
          <td style="padding: 32px 36px 24px; border-bottom: 1px solid #EFECE6; text-align: left;">
            <div style="font-family: Georgia, 'Times New Roman', serif; font-size: 17px; letter-spacing: 2.5px; text-transform: uppercase; color: #1E1B18; font-weight: 500;">Twinklebell</div>
            <div style="font-size: 10px; letter-spacing: 1.8px; text-transform: uppercase; color: #8A8177; margin-top: 3px;">Confectionaries London · Studio Notification</div>
          </td>
        </tr>

        <!-- Main Body -->
        <tr>
          <td style="padding: 32px 36px;">
            <div style="font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; color: #8A8177; font-weight: 600;">Incoming Order</div>
            <h1 style="margin: 6px 0 0; font-family: Georgia, 'Times New Roman', serif; font-size: 24px; font-weight: normal; color: #1E1B18; line-height: 1.3;">
              Order #{order.order_number}
            </h1>
            <p style="margin: 8px 0 24px; font-size: 13px; color: #696158; line-height: 1.6;">
              A new order has been confirmed online and is ready for kitchen scheduling.
            </p>

            <!-- Metadata Summary Card -->
            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #FAFAF8; border: 1px solid #ECE7DF; border-radius: 6px; margin-bottom: 24px;">
              <tr>
                <td style="padding: 18px 20px;">
                  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="font-size: 13px;">
                    <tr>
                      <td style="color: #8A8177; padding: 5px 0;">Tracking Reference</td>
                      <td align="right" style="font-family: 'SFMono-Regular', Consolas, monospace; font-weight: 600; color: #1E1B18;">{order.tracking_id}</td>
                    </tr>
                    <tr>
                      <td style="color: #8A8177; padding: 5px 0;">Customer</td>
                      <td align="right" style="font-weight: 600; color: #1E1B18;">{order.customer_name}</td>
                    </tr>
                    <tr>
                      <td style="color: #8A8177; padding: 5px 0;">Email</td>
                      <td align="right" style="color: #1E1B18;">{order.customer_email}</td>
                    </tr>
                    <tr>
                      <td style="color: #8A8177; padding: 5px 0;">Contact Number</td>
                      <td align="right" style="color: #1E1B18;">{order.customer_phone or '—'}</td>
                    </tr>
                    <tr>
                      <td style="color: #8A8177; padding: 5px 0;">Preferred Date</td>
                      <td align="right" style="font-weight: 600; color: #1E1B18;">{order.preferred_delivery_date or 'Standard Schedule'}</td>
                    </tr>
                    <tr>
                      <td style="color: #8A8177; padding: 5px 0;">Delivery Address</td>
                      <td align="right" style="color: #1E1B18; max-width: 240px;">{order.delivery_address or 'Standard UK'}</td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>

            <!-- Bake Specifications -->
            <div style="font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; color: #8A8177; font-weight: 600; margin-bottom: 12px;">Bake Specifications</div>
            
            {snapshot_block_html}

            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="font-size: 13px; border-top: 1px solid #ECE7DF; margin-bottom: 24px;">
              <tr>
                <td style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; color: #696158;">Size &amp; Portions</td>
                <td align="right" style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; font-weight: 600; color: #1E1B18;">{order.cake_size}</td>
              </tr>
              <tr>
                <td style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; color: #696158;">Flavour</td>
                <td align="right" style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; font-weight: 600; color: #1E1B18;">{order.cake_flavour}</td>
              </tr>
              <tr>
                <td style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; color: #696158;">Colour Palette</td>
                <td align="right" style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; color: #1E1B18;">{order.cake_colour}</td>
              </tr>
              {custom_specs_html}
              <tr>
                <td style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; color: #696158;">Custom Inscription</td>
                <td align="right" style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; font-style: italic; color: #1E1B18;">{f'"{order.cake_message}"' if order.cake_message else 'None requested'}</td>
              </tr>
              {f'''<tr>
                <td style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; color: #8A8177;">Dietary / Allergen Notice</td>
                <td align="right" style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; color: #9A3412; font-weight: 600;">{order.dietary_notes}</td>
              </tr>''' if order.dietary_notes else ''}
              <tr>
                <td style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; color: #696158;">Payment Method</td>
                <td align="right" style="padding: 10px 0; border-bottom: 1px solid #F0ECE6; font-weight: 600; color: #1E1B18;">{'Payment on Delivery (COD)' if order.payment_method == 'COD' else 'Paid via Card (Stripe)'}</td>
              </tr>
              <tr>
                <td style="padding: 12px 0; color: #1E1B18; font-weight: 600;">{'Amount to Collect' if order.payment_method == 'COD' else 'Total Paid'}</td>
                <td align="right" style="padding: 12px 0; font-family: Georgia, serif; font-size: 16px; font-weight: 600; color: #1E1B18;">£{order.total_amount} GBP</td>
              </tr>
            </table>

            <!-- Action Button -->
            <div style="padding-top: 8px;">
              <a href="{admin_url}" style="display: inline-block; background-color: #1E1B18; color: #FFFFFF; font-size: 12px; font-weight: 600; letter-spacing: 0.8px; text-decoration: none; padding: 13px 26px; border-radius: 4px; text-transform: uppercase;">
                Open Kitchen Dashboard &rarr;
              </a>
            </div>

            <div style="margin-top: 24px; font-size: 12px; color: #8A8177;">
              Customer tracker: <a href="{track_url}" style="color: #696158; text-decoration: underline;">{track_url}</a>
            </div>

          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="padding: 24px 36px; background-color: #FAFAF8; border-top: 1px solid #EFECE6; font-size: 11px; color: #8A8177; line-height: 1.6;">
            Twinklebell Confectionaries London &middot; 32d Grosvenor Road, Westcliff-on-Sea, SS0 8EN<br>
            Internal Kitchen Notification System
          </td>
        </tr>

      </table>
    </td>
  </tr>
</table>
</body>
</html>"""

            msg = EmailMultiAlternatives(
                subject=subject,
                body=plain_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[admin_email]
            )
            msg.attach_alternative(admin_html, "text/html")
            msg.send(fail_silently=False)
            print(f"[EMAIL SENT] Minimalist Admin alert sent to {admin_email}")
    except Exception as e:
        logger.error(f"Failed to send admin order notification: {e}")
        print(f"[EMAIL ERROR] Admin notification failed: {e}")


    # ========================================================
    # 2. CUSTOMER ORDER CONFIRMATION EMAIL
    # ========================================================
    try:
        if order.customer_email and "example.com" not in order.customer_email:
            cust_subject = f"Order Confirmation #{order.order_number} — Twinklebell Confectionaries"
            
            cust_plain = f"""Dear {order.customer_name},

Thank you for your order with Twinklebell Confectionaries London.
Your order #{order.order_number} has been received and confirmed.

Your Tracking Reference: {order.tracking_id}
Total Paid: £{order.total_amount} GBP

You can follow your cake's live preparation in our kitchen at:
{track_url}

Order Summary:
- Size: {order.cake_size}
- Flavour: {order.cake_flavour}
- Palette: {order.cake_colour}
- Inscription: {order.cake_message or 'None'}
- Preferred Date: {order.preferred_delivery_date or 'Standard Schedule'}
- Delivery Address: {order.delivery_address or 'Standard UK Delivery'}

If you have any questions or bespoke requests, simply reply directly to this email.

Warm regards,
Twinklebell Confectionaries London
www.twinklebellconfectionaries.co.uk
"""

            cust_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Order Confirmation #{order.order_number}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #F6F4F0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; color: #1E1B18; -webkit-font-smoothing: antialiased;">
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #F6F4F0; padding: 40px 12px;">
  <tr>
    <td align="center">
      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 560px; background-color: #FFFFFF; border: 1px solid #E6E1DA; border-radius: 8px; overflow: hidden;">
        
        <!-- Brand Header -->
        <tr>
          <td style="padding: 36px 36px 28px; border-bottom: 1px solid #EFECE6; text-align: left;">
            <div style="font-family: Georgia, 'Times New Roman', serif; font-size: 19px; letter-spacing: 2.5px; text-transform: uppercase; color: #1E1B18; font-weight: 500;">Twinklebell</div>
            <div style="font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: #8A8177; margin-top: 4px;">Confectionaries London</div>
          </td>
        </tr>

        <!-- Salutation & Context -->
        <tr>
          <td style="padding: 36px 36px 28px;">
            <h1 style="margin: 0 0 12px; font-family: Georgia, 'Times New Roman', serif; font-size: 26px; font-weight: normal; color: #1E1B18; line-height: 1.25;">
              Thank you for your order.
            </h1>
            <p style="margin: 0 0 24px; font-size: 14px; color: #575047; line-height: 1.65;">
              Dear {order.customer_name}, we are pleased to confirm that your cake order has been scheduled in our London kitchen. Every cake is freshly baked to order using authentic British recipes.
            </p>

            <!-- Tracking Callout Box -->
            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #FAFAF8; border: 1px solid #EAE5DD; border-radius: 6px; margin-bottom: 28px;">
              <tr>
                <td style="padding: 20px 24px;">
                  <div style="font-size: 10px; letter-spacing: 1.6px; text-transform: uppercase; color: #8A8177; font-weight: 600;">Tracking Reference</div>
                  <div style="margin-top: 4px; font-family: 'SFMono-Regular', Consolas, monospace; font-size: 18px; font-weight: 600; letter-spacing: 1.5px; color: #1E1B18;">
                    {order.tracking_id}
                  </div>
                  <div style="margin-top: 4px; font-size: 12px; color: #7B7268;">
                    Order Reference: #{order.order_number}
                  </div>
                </td>
              </tr>
            </table>

            <!-- Order Details Table -->
            <div style="font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; color: #8A8177; font-weight: 600; margin-bottom: 12px;">Order Summary</div>
            
            {snapshot_block_html}

            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="font-size: 13px; border-top: 1px solid #ECE7DF; margin-bottom: 28px;">
              <tr>
                <td style="padding: 11px 0; border-bottom: 1px solid #F0ECE6; color: #696158;">Cake Size</td>
                <td align="right" style="padding: 11px 0; border-bottom: 1px solid #F0ECE6; font-weight: 600; color: #1E1B18;">{order.cake_size}</td>
              </tr>
              <tr>
                <td style="padding: 11px 0; border-bottom: 1px solid #F0ECE6; color: #696158;">Sponge Flavour</td>
                <td align="right" style="padding: 11px 0; border-bottom: 1px solid #F0ECE6; font-weight: 600; color: #1E1B18;">{order.cake_flavour}</td>
              </tr>
              <tr>
                <td style="padding: 11px 0; border-bottom: 1px solid #F0ECE6; color: #696158;">Palette &amp; Finish</td>
                <td align="right" style="padding: 11px 0; border-bottom: 1px solid #F0ECE6; color: #1E1B18;">{order.cake_colour}</td>
              </tr>
              {custom_specs_html}
              {f'''<tr>
                <td style="padding: 11px 0; border-bottom: 1px solid #F0ECE6; color: #696158;">Piped Inscription</td>
                <td align="right" style="padding: 11px 0; border-bottom: 1px solid #F0ECE6; font-style: italic; color: #1E1B18;">"{order.cake_message}"</td>
              </tr>''' if order.cake_message else ''}
              <tr>
                <td style="padding: 11px 0; border-bottom: 1px solid #F0ECE6; color: #696158;">Delivery Address</td>
                <td align="right" style="padding: 11px 0; border-bottom: 1px solid #F0ECE6; color: #1E1B18; max-width: 240px;">{order.delivery_address or 'Standard UK Delivery'}</td>
              </tr>
              <tr>
                <td style="padding: 11px 0; border-bottom: 1px solid #F0ECE6; color: #696158;">Requested Delivery Date</td>
                <td align="right" style="padding: 11px 0; border-bottom: 1px solid #F0ECE6; font-weight: 600; color: #1E1B18;">{order.preferred_delivery_date or 'Standard Fresh Bake'}</td>
              </tr>
              <tr>
                <td style="padding: 11px 0; border-bottom: 1px solid #F0ECE6; color: #696158;">Payment Method</td>
                <td align="right" style="padding: 11px 0; border-bottom: 1px solid #F0ECE6; font-weight: 600; color: #1E1B18;">{'Payment on Delivery (Cash / Card)' if order.payment_method == 'COD' else 'Paid via Card (Stripe)'}</td>
              </tr>
              <tr>
                <td style="padding: 14px 0 0; color: #1E1B18; font-weight: 600;">{'Amount to Pay on Delivery' if order.payment_method == 'COD' else 'Total Paid'}</td>
                <td align="right" style="padding: 14px 0 0; font-family: Georgia, serif; font-size: 17px; font-weight: 600; color: #1E1B18;">£{order.total_amount} GBP</td>
              </tr>
            </table>

            <!-- Primary Action -->
            <div style="padding-top: 4px;">
              <a href="{track_url}" style="display: inline-block; background-color: #1E1B18; color: #FFFFFF; font-size: 13px; font-weight: 600; letter-spacing: 0.5px; text-decoration: none; padding: 14px 30px; border-radius: 4px;">
                Track Live Order Progress &rarr;
              </a>
            </div>

            <p style="margin: 28px 0 0; font-size: 13px; color: #7B7268; line-height: 1.6;">
              Have questions about your order, dietary notes, or delivery timing? Simply reply directly to this email and our kitchen team will assist you.
            </p>

          </td>
        </tr>

        <!-- Discreet Brand Footer -->
        <tr>
          <td style="padding: 26px 36px; background-color: #FAFAF8; border-top: 1px solid #EFECE6; font-size: 11px; color: #8A8177; line-height: 1.65;">
            Twinklebell Confectionaries London &middot; 32d Grosvenor Road, Westcliff-on-Sea, SS0 8EN, United Kingdom<br>
            Handcrafted cakes baked fresh daily. &copy; 2026 Twinklebell Confectionaries London.
          </td>
        </tr>

      </table>
    </td>
  </tr>
</table>
</body>
</html>"""

            msg = EmailMultiAlternatives(
                subject=cust_subject,
                body=cust_plain,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[order.customer_email]
            )
            msg.attach_alternative(cust_html, "text/html")
            msg.send(fail_silently=False)
            print(f"[EMAIL SENT] Minimalist customer confirmation sent to {order.customer_email}")
    except Exception as e:
        logger.error(f"Failed to send customer confirmation: {e}")
        print(f"[EMAIL ERROR] Customer confirmation failed: {e}")
