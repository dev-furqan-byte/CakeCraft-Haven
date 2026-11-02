from django.contrib import admin
from .models import Category, Product, Order, OrderItem, SubscriptionLead

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_featured', 'is_subscription', 'created_at')
    list_filter = ('category', 'is_featured', 'is_subscription')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price', 'quantity', 'subtotal')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'tracking_id', 'customer_name', 'payment_method', 'status', 'baking_stage', 'progress_percentage', 'total_amount', 'created_at')
    list_editable = ('status', 'baking_stage', 'progress_percentage')
    list_filter = ('payment_method', 'status', 'baking_stage', 'created_at')
    search_fields = ('order_number', 'tracking_id', 'customer_name', 'customer_email', 'stripe_session_id')
    readonly_fields = ('order_number', 'tracking_id', 'stripe_session_id', 'stripe_payment_intent_id', 'created_at', 'updated_at')
    inlines = [OrderItemInline]


@admin.register(SubscriptionLead)
class SubscriptionLeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'frequency', 'created_at')
    list_filter = ('frequency', 'created_at')
    search_fields = ('full_name', 'email')
