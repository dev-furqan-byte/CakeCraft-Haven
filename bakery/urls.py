from django.urls import path
from . import views

urlpatterns = [
    # Storefront & Ordering
    path('', views.index, name='index'),
    path('order/<int:product_id>/', views.order_cake, name='order_cake'),
    path('buy/<int:product_id>/', views.order_cake, name='create_checkout_session'),
    
    # Customer Order Tracking
    path('track-order/', views.track_order, name='track_order'),
    
    # 3D Custom Cake Builder & Ordering
    path('make-your-own-cake/', views.make_your_own_cake, name='make_your_own_cake'),
    path('api/cake-pricing/', views.api_cake_pricing, name='api_cake_pricing'),
    path('api/order-custom-cake/', views.order_custom_cake, name='order_custom_cake'),
    
    # Stripe Payment Callbacks & Webhooks
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
    
    # Moments Subscription Lead
    path('subscribe/', views.subscribe_lead, name='subscribe_lead'),
    
    # Bakery Owner Admin Aliases
    path('bakery-admin/', views.admin_entry_point, name='bakery_admin_dashboard'),
    path('bakery-admin/login/', views.admin_login_view, name='admin_login_alias'),
    path('bakery-admin/logout/', views.admin_logout_view, name='admin_logout_alias'),
    path('bakery-admin/update/<int:order_id>/', views.bakery_admin_update_order, name='admin_update_order_alias'),
]
