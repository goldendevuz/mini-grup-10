from django.contrib import admin
from .models.auth_models import User
from .models.models import Product, Compare, ProductComment, Promotion, CartItem, Category, Contact, Cart
# Register your models here.
admin.site.register(User)
