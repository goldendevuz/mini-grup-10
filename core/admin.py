from django.contrib import admin
from .models.auth_models import User
from .models.models import Product, Compare, ProductComment, Promotion, CartItem, Category, Contact, Cart

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Compare)
admin.site.register(ProductComment)
admin.site.register(Promotion)
admin.site.register(CartItem)
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(Cart)
