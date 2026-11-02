import uuid
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)  # In GBP (£)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    static_image_name = models.CharField(max_length=100, blank=True, help_text="e.g. twinklebell_2.jpeg")
    is_featured = models.BooleanField(default=True)
    is_subscription = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - £{self.price}"

    def get_image_url(self):
        if self.image:
            return self.image.url
        if self.static_image_name:
            return f"/static/images/{self.static_image_name}"
        return "/static/images/logo.png"

    @property
    def price_in_cents(self):
        return int(self.price * 100)


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Payment'),
        ('PAID', 'Payment Received (Paid)'),
        ('PROCESSING', 'Processing & Baking'),
        ('SHIPPED', 'Dispatched / Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Payment on Delivery'),
        ('STRIPE', 'Card Payment (Stripe)'),
    ]

    BAKING_STAGES = [
        ('ORDER_CONFIRMED', '1. Order Confirmed'),
        ('PREPARING', '2. Preparing & Baking'),
        ('SHIPPING', '3. Shipping / Out for Delivery'),
        ('DELIVERED', '4. Delivered & Completed'),
    ]

    ORDER_TYPE_CHOICES = [
        ('STANDARD', 'Standard Catalog Cake'),
        ('CUSTOM', 'Make Your Own (3D Custom Cake)'),
    ]

    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default='STANDARD')
    custom_cake_config = models.JSONField(blank=True, null=True, help_text="Full 3D cake design specification")
    custom_cake_snapshot = models.ImageField(upload_to='custom_cake_snapshots/', blank=True, null=True, help_text="Rendered 3D preview snapshot")

    order_number = models.CharField(max_length=64, unique=True, editable=False)
    tracking_id = models.CharField(max_length=64, blank=True, default='')
    
    # Customer Details
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=30, blank=True)
    delivery_address = models.TextField(blank=True)
    special_notes = models.TextField(blank=True)

    # Advanced Cake Customization
    cake_size = models.CharField(max_length=100, default='Standard (8-10 Servings)')
    cake_flavour = models.CharField(max_length=100, default='Classic Victoria Sponge')
    cake_colour = models.CharField(max_length=100, default='Classic Cream & Soft Gold')
    cake_message = models.CharField(max_length=255, blank=True, help_text="e.g. Happy Birthday Sarah!")
    quantity = models.PositiveIntegerField(default=1)
    reference_image = models.ImageField(upload_to='order_references/', blank=True, null=True)
    preferred_delivery_date = models.CharField(max_length=50, blank=True)
    dietary_notes = models.CharField(max_length=255, blank=True)

    # Live Cake Preparation Status (Managed by Admin)
    baking_stage = models.CharField(max_length=50, choices=BAKING_STAGES, default='ORDER_CONFIRMED')
    progress_percentage = models.PositiveIntegerField(default=25)
    estimated_completion = models.CharField(max_length=150, default="Fresh baking queue (Est. 24-48 hours)")
    baker_notes = models.TextField(blank=True, default="Order confirmed! Our London bakers are prepping the freshest ingredients.")
    
    # Financial & Payment
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='COD')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='gbp')
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    email_notification_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"TBC-{uuid.uuid4().hex[:8].upper()}"
        if not self.tracking_id:
            self.tracking_id = f"TRK-{uuid.uuid4().hex[:6].upper()}"

        # Automatic Stage <-> Status <-> Progress Synchronisation
        stage_to_progress = {
            'ORDER_CONFIRMED': 25,
            'PREPARING': 50,
            'SHIPPING': 75,
            'DELIVERED': 100,
        }

        # If Delivered
        if self.baking_stage == 'DELIVERED' or self.status == 'DELIVERED':
            self.baking_stage = 'DELIVERED'
            self.status = 'DELIVERED'
            self.progress_percentage = 100
        # If Shipping
        elif self.baking_stage == 'SHIPPING' or self.status == 'SHIPPED':
            self.baking_stage = 'SHIPPING'
            if self.status not in ['DELIVERED', 'CANCELLED']:
                self.status = 'SHIPPED'
            self.progress_percentage = max(75, self.progress_percentage)
        # If Preparing
        elif self.baking_stage == 'PREPARING' or self.status == 'PROCESSING':
            self.baking_stage = 'PREPARING'
            if self.status == 'PENDING':
                self.status = 'PROCESSING'
            self.progress_percentage = max(50, self.progress_percentage)
        # If Confirmed
        elif self.baking_stage == 'ORDER_CONFIRMED':
            self.progress_percentage = max(25, self.progress_percentage)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order_number} ({self.tracking_id}) - {self.customer_name}"

    def get_clean_phone(self):
        """Returns clean numeric phone string for WhatsApp links"""
        return "".join([c for c in self.customer_phone if c.isdigit()])

    @property
    def is_step1_done(self):
        return self.baking_stage in ['ORDER_CONFIRMED', 'PREPARING', 'SHIPPING', 'DELIVERED'] or self.progress_percentage >= 25

    @property
    def is_step2_done(self):
        return self.baking_stage in ['PREPARING', 'SHIPPING', 'DELIVERED'] or self.progress_percentage >= 50

    @property
    def is_step3_done(self):
        return self.baking_stage in ['SHIPPING', 'DELIVERED'] or self.progress_percentage >= 75

    @property
    def is_step4_done(self):
        return self.baking_stage == 'DELIVERED' or self.progress_percentage >= 100


class OrderUpdateHistory(models.Model):
    order = models.ForeignKey(Order, related_name='history', on_delete=models.CASCADE)
    stage_name = models.CharField(max_length=150)
    note = models.TextField(blank=True)
    progress_percentage = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order.tracking_id} - {self.stage_name} ({self.created_at.strftime('%H:%M')})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product_name} in {self.order.order_number}"

    @property
    def subtotal(self):
        return self.price * self.quantity


class SubscriptionLead(models.Model):
    FREQUENCY_CHOICES = [
        ('Monthly', 'Monthly Box'),
        ('Every 2 Months', 'Every 2 Months'),
        ('Quarterly', 'Quarterly Box'),
    ]

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES, default='Monthly')
    celebration_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Subscription Lead: {self.full_name} ({self.frequency})"
