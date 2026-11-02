import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twinklebell.settings')
django.setup()

from bakery.models import Category, Product

# Categories
cats = [
    {
        'name': 'Cupcakes',
        'slug': 'cupcakes',
        'description': 'Miniature Victoria sponges with hand-piped buttercream.'
    },
    {
        'name': 'Maxi Loaf Cakes',
        'slug': 'maxi-loaf-cakes',
        'description': 'Moist British loaves in rotating seasonal flavours.'
    },
    {
        'name': 'Celebration Cakes',
        'slug': 'celebration-cakes',
        'description': 'Bespoke tiered and single celebration cakes for special occasions.'
    },
    {
        'name': 'Cake & Cream Packages',
        'slug': 'cake-and-cream-packages',
        'description': 'Artisan sponges paired with fresh clotted cream.'
    },
]

category_objs = {}
for c in cats:
    obj, _ = Category.objects.get_or_create(slug=c['slug'], defaults={'name': c['name'], 'description': c['description']})
    category_objs[c['slug']] = obj

# Products
prods = [
    {
        'category': category_objs['cupcakes'],
        'name': 'Hand-Piped Victoria Sponge Cupcakes (Box of 6)',
        'slug': 'hand-piped-victoria-sponge-cupcakes',
        'tagline': 'Cloud-light sponge with vanilla buttercream',
        'description': 'Cloud-light Victoria sponge in miniature — crowned with hand-piped buttercream and finished with the kind of care you can taste.',
        'price': 18.00,
        'static_image_name': 'twinklebell_3.jpeg',
        'is_featured': True,
    },
    {
        'category': category_objs['maxi-loaf-cakes'],
        'name': 'Artisan Zesty Maxi Loaf Cake',
        'slug': 'artisan-zesty-maxi-loaf-cake',
        'tagline': 'Generously moist with seasonal zesty glaze',
        'description': 'Generously moist loaves in rotating seasonal flavours — lemon drizzle, carrot & spice, chocolate sponge. Ideal for gifting, or keeping entirely to yourself.',
        'price': 22.00,
        'static_image_name': 'twinklebell_5.jpeg',
        'is_featured': True,
    },
    {
        'category': category_objs['celebration-cakes'],
        'name': 'Bespoke Tiered Celebration Cake',
        'slug': 'bespoke-tiered-celebration-cake',
        'tagline': 'Custom made for birthdays, weddings & milestones',
        'description': 'Bespoke single and tiered sponge cakes for birthdays, weddings, and every milestone that deserves more than a supermarket shelf.',
        'price': 65.00,
        'static_image_name': 'twinklebell_4.jpeg',
        'is_featured': True,
    },
    {
        'category': category_objs['cake-and-cream-packages'],
        'name': 'Signature Cake & Clotted Cream Package',
        'slug': 'signature-cake-clotted-cream-package',
        'tagline': 'Signature sponge paired with artisan clotted cream',
        'description': 'Our signature sponge cakes paired with artisan clotted cream — a proper British indulgence, beautifully boxed and ready to delight.',
        'price': 32.00,
        'static_image_name': 'twinklebell_6.jpeg',
        'is_featured': True,
    },
]

for p in prods:
    obj, created = Product.objects.get_or_create(
        slug=p['slug'],
        defaults=p
    )
    if created:
        print(f"Created Product: {obj.name} (£{obj.price})")
    else:
        print(f"Product already exists: {obj.name}")

print("Database seeding completed successfully!")

