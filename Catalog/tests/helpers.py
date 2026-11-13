from user.models import User
from Catalog.models import Category, Brand, Product

import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile







def InitUsers():
    # create user and admin
    user = User.objects.create(
        username='user',
        email='user123@gmail.com',
        password='user123'
    )
    admin = User.objects.create(
        username='admin',
        email='admin123@gmail.com', 
        password='admin123',
        is_staff=True
    )

    return user, admin

def InitCategories():
    # create categories
    cat1 = Category.objects.create(
        name='Electronics',
        description="All Electronic from a fan to phone",
        parent=None,
        is_active=True
    )

    cat2 = Category.objects.create(
        name='Sports',
        description="All Sports items",
        parent=None,
        is_active=True
    )

    return cat1, cat2

def InitBrands():
    ''' Create Demo Brand models objects '''
    brand1 = Brand.objects.create(
        name='Dell',
        description='Best Computer and Laptop',
        logo='dell.png',
        is_active=True,
    )
    brand2 = Brand.objects.create(
        name='Nike',
        description='Best Sport and Casual Shoes',
        logo='NIke.png',
        is_active=True,
    )

    return brand1, brand2

def get_test_image():
    file = io.BytesIO()
    image = Image.new("RGB", (100, 100), color="red")
    image.save(file, format="PNG")
    file.seek(0)
    return SimpleUploadedFile(
        name="logo.png",
        content=file.read(),
        content_type="image/png",
    )

def InitProducts():
    elec, sport = InitCategories()
    dell, nike = InitBrands()

    product1 = Product.objects.create(
        name='Dell latidue 7390',
        description='Dell notebook size best laptop',
        is_active=True,
        category=elec, 
        brand=dell,
        base_price=35000,
        discount_price=27000
    )

    product2 = Product.objects.create(
        name='Nike sports shoes',
        description="Best sports shoes",
        is_active=True,
        category=sport, 
        brand=nike,
        base_price=35000,
        discount_price=27000
    )

    return product1, product2




