import json
import uuid
import csv
import base64
import stripe
from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from .models import Category, Product, Order, OrderItem, SubscriptionLead, OrderUpdateHistory
from .emails import send_order_emails
from .cake_pricing import calculate_custom_cake_price, get_full_catalog_context

stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    """Main landing page replicating Twinklebell Confectionaries"""
    categories = Category.objects.all()
    products = Product.objects.filter(is_featured=True)
    
    gallery_images = [
        {'src': '/static/images/twinklebell_2.jpeg', 'alt': 'Artisan British Sponge Cake'},
        {'src': '/static/images/twinklebell_3.jpeg', 'alt': 'Hand-piped Buttercream Cupcakes'},
        {'src': '/static/images/twinklebell_4.jpeg', 'alt': 'Celebration Milestone Cake'},
        {'src': '/static/images/twinklebell_5.jpeg', 'alt': 'Zesty Lemon Drizzle Maxi Loaf'},
        {'src': '/static/images/twinklebell_6.jpeg', 'alt': 'Artisan Cake and Cream Package'},
        {'src': '/static/images/twinklebell_7.jpeg', 'alt': 'Tiered Celebration Cake'},
        {'src': '/static/images/twinklebell_8.jpeg', 'alt': 'Fresh Baked Sponge Slices'},
        {'src': '/static/images/twinklebell_9.jpeg', 'alt': 'Festive Handcrafted Cakes'},
    ]

    context = {
        'categories': categories,
        'products': products,
        'gallery_images': gallery_images,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'bakery/index.html', context)


def order_cake(request, product_id):
    """
    Advanced Cake Order Form (Guest Checkout - No Login Needed)
    Collects cake customizations, reference image, customer contact, and proceeds to Stripe.
    """
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Customer Info
        customer_name = request.POST.get('customer_name', '').strip()
        customer_email = request.POST.get('customer_email', '').strip()
        customer_phone = request.POST.get('customer_phone', '').strip()
        delivery_address = request.POST.get('delivery_address', '').strip()
        special_notes = request.POST.get('special_notes', '').strip()

        # Advanced Cake Customization
        cake_size = request.POST.get('cake_size', 'Standard (8-10 Servings)')
        cake_flavour = request.POST.get('cake_flavour', 'Classic Victoria Sponge')
        cake_colour = request.POST.get('cake_colour', 'Classic Cream & Soft Gold')
        cake_message = request.POST.get('cake_message', '').strip()
        preferred_delivery_date = request.POST.get('preferred_delivery_date', '').strip()
        dietary_notes = request.POST.get('dietary_notes', '').strip()
        
        try:
            quantity = max(1, int(request.POST.get('quantity', 1)))
        except ValueError:
            quantity = 1

        reference_image = request.FILES.get('reference_image')

        # Size surcharge (e.g. larger sizes)
        size_multiplier = 1.0
        if 'Large' in cake_size or '15-20' in cake_size:
            size_multiplier = 1.35
        elif 'Tiered' in cake_size or '25+' in cake_size:
            size_multiplier = 1.8

        item_unit_price = round(float(product.price) * size_multiplier, 2)
        total_amount = round(item_unit_price * quantity, 2)

        scheme = 'https' if request.is_secure() else 'http'
        host = request.get_host()
        domain_url = f"{scheme}://{host}"

        payment_method = request.POST.get('payment_method', 'COD').upper()

        try:
            # 1. Create Order in Database
            order = Order.objects.create(
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                delivery_address=delivery_address,
                special_notes=special_notes,
                cake_size=cake_size,
                cake_flavour=cake_flavour,
                cake_colour=cake_colour,
                cake_message=cake_message,
                quantity=quantity,
                reference_image=reference_image,
                preferred_delivery_date=preferred_delivery_date,
                dietary_notes=dietary_notes,
                total_amount=total_amount,
                currency=settings.STRIPE_CURRENCY,
                payment_method=payment_method,
                status='PENDING',
                baking_stage='ORDER_CONFIRMED',
                progress_percentage=25,
                estimated_completion="Fresh baking scheduled (Est. 24-48 hours)",
                baker_notes="Order confirmed via Payment on Delivery. Payment will be collected upon arrival." if payment_method == 'COD' else "Order submitted online. Awaiting Stripe payment confirmation.",
            )

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=f"{product.name} ({cake_size})",
                price=item_unit_price,
                quantity=quantity
            )

            # Option A: Payment on Delivery (COD) -> Instant Confirmation
            if payment_method == 'COD':
                try:
                    send_order_emails(order, request)
                    order.email_notification_sent = True
                    order.save(update_fields=['email_notification_sent'])
                except Exception as email_err:
                    print(f"[EMAIL TRIGGER NOTICE] COD order email: {email_err}")

                try:
                    messages.success(request, f"Order #{order.order_number} confirmed! Pay on delivery upon arrival.", fail_silently=True)
                except Exception:
                    pass
                return redirect(f"{domain_url}/payment/success/?order_id={order.id}")

            # Option B: Online Card Payment via Stripe
            line_item_data = {
                'price_data': {
                    'currency': settings.STRIPE_CURRENCY,
                    'unit_amount': int(item_unit_price * 100),
                    'product_data': {
                        'name': f"{product.name} — {cake_size}",
                        'description': f"Flavour: {cake_flavour} | Inscription: {cake_message or 'None'}"[:250],
                    },
                },
                'quantity': quantity,
            }

            checkout_session = stripe.checkout.Session.create(
                customer_email=customer_email,
                payment_method_types=['card'],
                billing_address_collection='required',
                managed_payments={'enabled': False},
                line_items=[line_item_data],
                mode='payment',
                success_url=f"{domain_url}/payment/success/?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{domain_url}/payment/cancel/?order_id={order.id}",
                metadata={
                    'order_id': order.id,
                    'order_number': order.order_number,
                    'tracking_id': order.tracking_id,
                    'product_id': product.id,
                }
            )

            order.stripe_session_id = checkout_session.id
            order.save(update_fields=['stripe_session_id'])

            # Send Instant Email Notification
            try:
                send_order_emails(order, request)
                order.email_notification_sent = True
                order.save(update_fields=['email_notification_sent'])
            except Exception as email_err:
                print(f"[EMAIL TRIGGER NOTICE] Initial order email: {email_err}")

            return redirect(checkout_session.url, code=303)

        except Exception as e:
            try:
                messages.error(request, f"Error processing order: {e}", fail_silently=True)
            except Exception:
                pass
            return render(request, 'bakery/order_cake.html', {'product': product, 'error': str(e)})

    return render(request, 'bakery/order_cake.html', {'product': product})


def make_your_own_cake(request):
    """
    Interactive 3D 'Make Your Own Cake' Studio.
    Lets customers customize shape, tiers, flavors, fillings, frostings,
    colors, drips, toppings, live inscription text, board, and extras in real-time 3D.
    """
    catalog = get_full_catalog_context()
    context = {
        'catalog': catalog,
        'catalog_json': json.dumps(catalog),
    }
    return render(request, 'bakery/make_your_own_cake.html', context)


def api_cake_pricing(request):
    """
    JSON API for dynamic price calculation and breakdown validation.
    Accepts config via POST (JSON or form data) and returns server-validated total.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        if request.content_type == 'application/json':
            config = json.loads(request.body.decode('utf-8'))
        else:
            raw_config = request.POST.get('config', '{}')
            config = json.loads(raw_config) if isinstance(raw_config, str) else raw_config
    except Exception as e:
        return JsonResponse({'error': f'Invalid config format: {e}'}, status=400)

    total_price, breakdown = calculate_custom_cake_price(config)
    return JsonResponse({
        'success': True,
        'total_price': total_price,
        'breakdown': breakdown,
    })


def order_custom_cake(request):
    """
    Handles submission of custom 3D cake orders.
    Validates configuration and server price, saves 3D canvas snapshot,
    creates Order (order_type='CUSTOM'), and routes to COD or Stripe checkout.
    """
    if request.method != 'POST':
        return redirect('make_your_own_cake')

    try:
        # 1. Parse Configuration
        raw_config = request.POST.get('config', '{}')
        try:
            config = json.loads(raw_config) if isinstance(raw_config, str) else raw_config
        except Exception:
            config = {}

        # 2. Server-side Price Recomputation (NEVER TRUST CLIENT)
        total_price, breakdown = calculate_custom_cake_price(config)

        # 3. Customer Contact Info
        customer_name = request.POST.get('customer_name', '').strip()
        customer_email = request.POST.get('customer_email', '').strip()
        customer_phone = request.POST.get('customer_phone', '').strip()
        delivery_address = request.POST.get('delivery_address', '').strip()
        preferred_delivery_date = request.POST.get('preferred_delivery_date', '').strip()
        special_notes = request.POST.get('special_notes', '').strip()
        payment_method = request.POST.get('payment_method', 'COD').upper()

        if not customer_name or not customer_email:
            try:
                messages.error(request, "Please enter your name and email address.", fail_silently=True)
            except Exception:
                pass
            return redirect('make_your_own_cake')

        # 4. Process 3D Canvas Snapshot
        snapshot_file = None
        snapshot_data = request.POST.get('snapshot_data', '')
        if snapshot_data and 'base64,' in snapshot_data:
            try:
                format_prefix, imgstr = snapshot_data.split('base64,')
                ext = 'png'
                data = base64.b64decode(imgstr)
                file_name = f"3d_cake_{uuid.uuid4().hex[:10]}.{ext}"
                snapshot_file = ContentFile(data, name=file_name)
            except Exception as snap_err:
                print(f"[SNAPSHOT PROCESS NOTICE]: {snap_err}")

        # Human-readable specs
        shape_name = config.get('shape', 'round').title()
        tiers_count = int(config.get('tiers', 1))
        weight_label = config.get('weight', '1kg').upper()
        sponge_flv = config.get('sponge_flavor', 'vanilla').replace('_', ' ').title()
        frosting_clr = config.get('frosting_color', '#FFF8F0')
        cake_msg = config.get('message_text', '').strip()

        # 5. Create Custom Cake Order
        order = Order.objects.create(
            order_type='CUSTOM',
            custom_cake_config=config,
            custom_cake_snapshot=snapshot_file,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            delivery_address=delivery_address,
            special_notes=special_notes,
            preferred_delivery_date=preferred_delivery_date,
            cake_size=f"{tiers_count}-Tier {shape_name} ({weight_label})",
            cake_flavour=sponge_flv,
            cake_colour=frosting_clr,
            cake_message=cake_msg,
            quantity=1,
            total_amount=total_price,
            currency=settings.STRIPE_CURRENCY,
            payment_method=payment_method,
            status='PENDING',
            baking_stage='ORDER_CONFIRMED',
            progress_percentage=25,
            estimated_completion="Fresh 3D custom bake scheduled (Est. 24-48 hours)",
            baker_notes=f"Custom 3D Cake Design ({tiers_count} Tier {shape_name}). Handcrafted to customer's exact 3D specification.",
        )

        OrderItem.objects.create(
            order=order,
            product=None,
            product_name=f"Custom 3D Cake ({shape_name} · {tiers_count} Tier · {weight_label})",
            price=total_price,
            quantity=1
        )

        scheme = 'https' if request.is_secure() else 'http'
        host = request.get_host()
        domain_url = f"{scheme}://{host}"

        # Option A: Cash on Delivery (COD) -> Instant Confirmation
        if payment_method == 'COD':
            try:
                send_order_emails(order, request)
                order.email_notification_sent = True
                order.save(update_fields=['email_notification_sent'])
            except Exception as email_err:
                print(f"[EMAIL TRIGGER NOTICE] COD custom cake email: {email_err}")

            try:
                messages.success(request, f"Custom Cake Order #{order.order_number} confirmed! Pay on delivery upon arrival.", fail_silently=True)
            except Exception:
                pass
            return redirect(f"{domain_url}/payment/success/?order_id={order.id}")

        # Option B: Online Card Payment via Stripe
        line_item_data = {
            'price_data': {
                'currency': settings.STRIPE_CURRENCY,
                'unit_amount': int(total_price * 100),
                'product_data': {
                    'name': f"Custom 3D Cake ({shape_name} · {tiers_count} Tier)",
                    'description': f"Sponge: {sponge_flv} | Message: {cake_msg or 'None'}"[:250],
                },
            },
            'quantity': 1,
        }

        checkout_session = stripe.checkout.Session.create(
            customer_email=customer_email,
            payment_method_types=['card'],
            billing_address_collection='required',
            managed_payments={'enabled': False},
            line_items=[line_item_data],
            mode='payment',
            success_url=f"{domain_url}/payment/success/?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{domain_url}/payment/cancel/?order_id={order.id}",
            metadata={
                'order_id': order.id,
                'order_number': order.order_number,
                'tracking_id': order.tracking_id,
                'order_type': 'CUSTOM',
            }
        )

        order.stripe_session_id = checkout_session.id
        order.save(update_fields=['stripe_session_id'])

        try:
            send_order_emails(order, request)
            order.email_notification_sent = True
            order.save(update_fields=['email_notification_sent'])
        except Exception as email_err:
            print(f"[EMAIL TRIGGER NOTICE] Initial order email: {email_err}")

        return redirect(checkout_session.url, code=303)

    except Exception as e:
        try:
            messages.error(request, f"Error creating custom order: {e}", fail_silently=True)
        except Exception:
            pass
        return redirect('make_your_own_cake')


def track_order(request):
    """
    Live Customer Order Tracking
    Allows customers to paste their Order Tracking ID and see live progress.
    """
    tracking_id = request.GET.get('tracking_id', '').strip()
    order = None
    not_found = False

    if tracking_id:
        # Search by tracking_id or order_number
        order = Order.objects.filter(tracking_id__iexact=tracking_id).first()
        if not order:
            order = Order.objects.filter(order_number__iexact=tracking_id).first()
        if not order:
            not_found = True

    context = {
        'order': order,
        'tracking_id': tracking_id,
        'not_found': not_found,
    }
    return render(request, 'bakery/track_order.html', context)


def payment_success(request):
    """Payment success / order confirmation callback page for both Stripe & Cash on Delivery"""
    session_id = request.GET.get('session_id')
    order_id = request.GET.get('order_id')
    order = None

    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            meta_order_id = session.metadata.get('order_id')
            
            if meta_order_id:
                order = Order.objects.filter(id=meta_order_id).first()
            if not order:
                order = Order.objects.filter(stripe_session_id=session_id).first()

            if order:
                order.status = 'PAID'
                order.payment_method = 'STRIPE'
                order.stripe_payment_intent_id = session.payment_intent or ''
                order.baking_stage = 'PREPARING'
                order.progress_percentage = 50
                order.baker_notes = "Payment verified via Stripe! Ingredients selected and baking has commenced."
                order.save()

                if not order.email_notification_sent:
                    send_order_emails(order, request)
                    order.email_notification_sent = True
                    order.save(update_fields=['email_notification_sent'])
        except Exception as e:
            print(f"Error verifying Stripe session: {e}")

    elif order_id:
        order = Order.objects.filter(id=order_id).first()

    return render(request, 'bakery/payment_success.html', {'order': order, 'session_id': session_id})


def payment_cancel(request):
    """Payment cancel page"""
    order_id = request.GET.get('order_id')
    order = None
    if order_id:
        order = Order.objects.filter(id=order_id).first()
        if order and order.status == 'PENDING':
            order.status = 'CANCELLED'
            order.save(update_fields=['status'])

    return render(request, 'bakery/payment_cancel.html', {'order': order})


@csrf_exempt
def stripe_webhook(request):
    """Stripe webhook to handle events asynchronously"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    event = None
    try:
        if endpoint_secret:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        else:
            event = json.loads(payload)
    except Exception as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session.get('metadata', {}).get('order_id')
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                order.status = 'PAID'
                order.stripe_payment_intent_id = session.get('payment_intent', '')
                order.save()
                if not order.email_notification_sent:
                    send_order_emails(order)
                    order.email_notification_sent = True
                    order.save(update_fields=['email_notification_sent'])
            except Order.DoesNotExist:
                pass

    return HttpResponse(status=200)


def subscribe_lead(request):
    """Handle subscription form from Moments section"""
    if request.method == 'POST':
        name = request.POST.get('full_name')
        email = request.POST.get('email')
        frequency = request.POST.get('frequency', 'Monthly')
        notes = request.POST.get('celebration_notes', '')

        if name and email:
            SubscriptionLead.objects.create(
                full_name=name,
                email=email,
                frequency=frequency,
                celebration_notes=notes
            )
            messages.success(request, "Thank you! Your subscription inquiry has been received. We'll be in touch shortly!")
        else:
            messages.error(request, "Please enter your name and email.")

    return redirect('/#moments')


# ========================================================
# PROPER HEAVY BAKERY ADMIN DASHBOARD (/admin/)
# ========================================================

def admin_entry_point(request):
    """
    Main entry point for /admin/
    If not logged in: Shows clean staff login page.
    If logged in as staff: Displays the full, heavy Bakery Management Dashboard!
    """
    if request.user.is_authenticated and request.user.is_staff:
        return bakery_admin_dashboard(request)

    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}! Bakery Dashboard loaded.")
            return redirect('/admin/')
        else:
            messages.error(request, "Invalid username or password. Staff access only.")

    return render(request, 'bakery/admin_login.html')


def admin_login_view(request):
    """Staff login page"""
    return admin_entry_point(request)


def admin_logout_view(request):
    """Staff logout"""
    logout(request)
    messages.info(request, "You have been logged out of the Bakery Dashboard.")
    return redirect('/admin/')


def is_staff_check(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_staff_check, login_url='/admin/')
def bakery_admin_dashboard(request):
    """
    Proper Heavy Executive Dashboard for Bakery Owner & Staff.
    Shows all orders, live baking status, revenue metrics, customer customizations,
    catalog products, and subscription leads.
    """
    all_orders = Order.objects.all().order_by('-created_at')
    
    # KPIs & Metrics
    total_orders = all_orders.count()
    paid_orders = all_orders.filter(status='PAID').count()
    baking_orders = all_orders.filter(baking_stage='PREPARING').count()
    dispatched_orders = all_orders.filter(baking_stage='SHIPPING').count()
    completed_orders = all_orders.filter(baking_stage='DELIVERED').count()
    total_revenue = sum(o.total_amount for o in all_orders.filter(status__in=['PAID', 'PROCESSING', 'SHIPPED', 'DELIVERED']))

    # Search & Filter
    orders = all_orders
    search_q = request.GET.get('q', '').strip()
    if search_q:
        orders = orders.filter(
            Q(tracking_id__icontains=search_q) |
            Q(order_number__icontains=search_q) |
            Q(customer_name__icontains=search_q) |
            Q(customer_email__icontains=search_q) |
            Q(customer_phone__icontains=search_q)
        )

    filter_status = request.GET.get('status')
    if filter_status:
        orders = orders.filter(status=filter_status)

    filter_stage = request.GET.get('stage')
    if filter_stage:
        orders = orders.filter(baking_stage=filter_stage)

    filter_type = request.GET.get('type')
    if filter_type:
        orders = orders.filter(order_type=filter_type)

    custom_orders_count = all_orders.filter(order_type='CUSTOM').count()

    # Products & Subscription Leads
    products = Product.objects.all().order_by('category', 'name')
    subscription_leads = SubscriptionLead.objects.all().order_by('-created_at')

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'paid_orders': paid_orders,
        'baking_orders': baking_orders,
        'dispatched_orders': dispatched_orders,
        'completed_orders': completed_orders,
        'custom_orders_count': custom_orders_count,
        'total_revenue': total_revenue,
        'baking_stages': Order.BAKING_STAGES,
        'status_choices': Order.STATUS_CHOICES,
        'search_q': search_q,
        'filter_status': filter_status,
        'filter_stage': filter_stage,
        'filter_type': filter_type,
        'products': products,
        'subscription_leads': subscription_leads,
    }
    return render(request, 'bakery/admin_dashboard.html', context)


@user_passes_test(is_staff_check, login_url='/admin/')
def bakery_admin_update_order(request, order_id):
    """
    Simple & friendly order update for bakery owner / staff.
    Automatically handles stage progress and customer tracker synchronization.
    """
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_stage = request.POST.get('baking_stage', order.baking_stage)
        order.baking_stage = new_stage

        if 'status' in request.POST and request.POST.get('status'):
            order.status = request.POST.get('status')
            
        if 'estimated_completion' in request.POST:
            order.estimated_completion = request.POST.get('estimated_completion')
            
        if 'baker_notes' in request.POST:
            order.baker_notes = request.POST.get('baker_notes')

        order.save()

        # Log history event
        OrderUpdateHistory.objects.create(
            order=order,
            stage_name=dict(Order.BAKING_STAGES).get(order.baking_stage, order.baking_stage),
            note=order.baker_notes,
            progress_percentage=order.progress_percentage
        )

        messages.success(request, f"Order #{order.order_number} ({order.customer_name}) updated successfully!")
        return redirect('/admin/')

    return redirect('/admin/')


@user_passes_test(is_staff_check, login_url='/admin/')
def print_kitchen_ticket(request, order_id):
    """
    Printable Kitchen Bake Slip / Chef Ticket
    Clean, high-legibility ticket for pastry chefs to stick to cake boards / boxes.
    """
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'bakery/kitchen_ticket.html', {'order': order})


@user_passes_test(is_staff_check, login_url='/admin/')
def export_orders_csv(request):
    """
    Export all orders to Excel-compatible CSV file
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="twinklebell_orders.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Tracking ID', 'Order Number', 'Date', 'Customer Name', 'Email', 'Phone',
        'Delivery Address', 'Cake Size', 'Flavour', 'Colour', 'Inscription Message',
        'Quantity', 'Amount (GBP)', 'Status', 'Kitchen Stage', 'Allergens/Notes'
    ])

    for o in Order.objects.all().order_by('-created_at'):
        writer.writerow([
            o.tracking_id, o.order_number, o.created_at.strftime('%Y-%m-%d %H:%M'),
            o.customer_name, o.customer_email, o.customer_phone, o.delivery_address,
            o.cake_size, o.cake_flavour, o.cake_colour, o.cake_message,
            o.quantity, o.total_amount, o.status, o.get_baking_stage_display(), o.dietary_notes
        ])

    return response


@user_passes_test(is_staff_check, login_url='/admin/')
def admin_create_product(request):
    """
    Quick Add New Cake Product directly from the Dashboard
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category_id = request.POST.get('category_id')
        price = request.POST.get('price', 0)
        tagline = request.POST.get('tagline', '').strip()
        description = request.POST.get('description', '').strip()
        image = request.FILES.get('image')

        if name and category_id and price:
            category = get_object_or_404(Category, id=category_id)
            slug = f"{name.lower().replace(' ', '-')}-{uuid.uuid4().hex[:4]}"
            Product.objects.create(
                category=category,
                name=name,
                slug=slug,
                tagline=tagline,
                description=description,
                price=float(price),
                image=image,
                is_featured=True
            )
            messages.success(request, f"New Cake '{name}' added successfully to the menu!")
        else:
            messages.error(request, "Please enter all required cake details.")

    return redirect('/admin/')


@user_passes_test(is_staff_check, login_url='/admin/')
def admin_quick_status(request, order_id, new_status):
    """Simple 1-click status or stage updater for non-technical bakery staff"""
    order = get_object_or_404(Order, id=order_id)
    
    # Check if stage
    if new_status in dict(Order.BAKING_STAGES):
        order.baking_stage = new_status
        order.save()
        OrderUpdateHistory.objects.create(
            order=order,
            stage_name=dict(Order.BAKING_STAGES).get(new_status, new_status),
            note=f"Stage updated to {dict(Order.BAKING_STAGES).get(new_status, new_status)}",
            progress_percentage=order.progress_percentage
        )
        messages.success(request, f"Order #{order.order_number} moved to: {dict(Order.BAKING_STAGES).get(new_status)}!")
    elif new_status in dict(Order.STATUS_CHOICES):
        order.status = new_status
        order.save()
        messages.success(request, f"Order #{order.order_number} marked as: {new_status}!")
        
    return redirect('/admin/')


@user_passes_test(is_staff_check, login_url='/admin/')
def admin_delete_order(request, order_id):
    """Delete order from dashboard"""
    order = get_object_or_404(Order, id=order_id)
    ref = order.order_number
    order.delete()
    messages.warning(request, f"Order #{ref} was permanently deleted.")
    return redirect('/admin/')
