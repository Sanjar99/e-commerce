# check_admin_setup.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("=" * 80)
print("DJANGO ADMIN PANEL SOZLAMALARI TEKSHIRISH")
print("=" * 80)

# 1. INSTALLED_APPS tekshirish
from django.conf import settings

print("\n1️⃣ INSTALLED APPS:")
for i, app in enumerate(settings.INSTALLED_APPS, 1):
    if 'django' not in app:
        print(f"   {i}. {app}")

# 2. AUTH_USER_MODEL tekshirish
print(f"\n2️⃣ AUTH_USER_MODEL: {getattr(settings, 'AUTH_USER_MODEL', 'NOT SET')}")

# 3. Admin site ro'yxatdan o'tgan modellar
from django.contrib import admin

print("\n3️⃣ ADMIN PANEL RO'YXATDAN O'TGAN MODELLAR:")

if hasattr(admin.site, '_registry') and admin.site._registry:
    for i, (model, model_admin) in enumerate(admin.site._registry.items(), 1):
        app_label = model._meta.app_label
        model_name = model._meta.model_name
        print(f"   {i}. {app_label}.{model_name}")
else:
    print("   ❌ Hech qanday model ro'yxatdan o'tmagan!")

# 4. App'larda admin.py mavjudligini tekshirish
print("\n4️⃣ ADMIN.PY FAYLLARI:")
apps_to_check = ['users', 'products', 'seller', 'staff']

for app in apps_to_check:
    admin_file = os.path.join(app, 'admin.py')
    if os.path.exists(admin_file):
        print(f"   ✅ {app}/admin.py - MAVJUD")
    else:
        print(f"   ❌ {app}/admin.py - MAVJUD EMAS")

# 5. Model importlarini tekshirish
print("\n5️⃣ MODEL IMPORTLARI:")
try:
    from users.models import User

    print("   ✅ users.models.User - MAVJUD")
except ImportError as e:
    print(f"   ❌ users.models.User - XATO: {e}")

try:
    from products.models import Product

    print("   ✅ products.models.Product - MAVJUD")
except ImportError as e:
    print(f"   ❌ products.models.Product - XATO: {e}")

try:
    from seller.models import Seller

    print("   ✅ seller.models.Seller - MAVJUD")
except ImportError as e:
    print(f"   ❌ seller.models.Seller - XATO: {e}")

# 6. Admin URL test
from django.urls import reverse

print("\n6️⃣ ADMIN URL'LAR:")
try:
    admin_url = reverse('admin:index')
    print(f"   ✅ Admin index URL: {admin_url}")

    # Test some model URLs
    test_models = [
        ('users', 'user'),
        ('products', 'product'),
        ('seller', 'seller'),
    ]

    for app, model in test_models:
        try:
            url = reverse(f'admin:{app}_{model}_changelist')
            print(f"   ✅ {app}.{model}: {url}")
        except:
            print(f"   ❌ {app}.{model}: URL mavjud emas")

except Exception as e:
    print(f"   ❌ URL test xatosi: {e}")

print("\n" + "=" * 80)
print("TEKSHIRISH TUGADI")
print("=" * 80)