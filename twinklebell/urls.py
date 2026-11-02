from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from bakery import views as bakery_views

urlpatterns = [
    # Custom Proper Heavy Bakery Admin at /admin/
    path('admin/', bakery_views.admin_entry_point, name='admin_home'),
    path('admin/login/', bakery_views.admin_login_view, name='admin_login'),
    path('admin/logout/', bakery_views.admin_logout_view, name='admin_logout'),
    path('admin/update/<int:order_id>/', bakery_views.bakery_admin_update_order, name='admin_update_order'),
    path('admin/order/status/<int:order_id>/<str:new_status>/', bakery_views.admin_quick_status, name='admin_quick_status'),
    path('admin/order/delete/<int:order_id>/', bakery_views.admin_delete_order, name='admin_delete_order'),
    
    # Advanced Admin Features (Print Ticket, Export CSV, Add Product)
    path('admin/order/print/<int:order_id>/', bakery_views.print_kitchen_ticket, name='print_kitchen_ticket'),
    path('admin/orders/export-csv/', bakery_views.export_orders_csv, name='export_orders_csv'),
    path('admin/product/create/', bakery_views.admin_create_product, name='admin_create_product'),

    # Standard Django Database Model Admin (accessible anytime)
    path('django-admin/', admin.site.urls),

    # Main Bakery Storefront & Tracking
    path('', include('bakery.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
