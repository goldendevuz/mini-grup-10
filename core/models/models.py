from django.db import models
from django.conf import settings

# Импортируем твою модель Firma из папки с юзерами.
# ВАЖНО: замени 'users.models' на реальное название твоей папки с пользователями!
from core.models.auth_models import Firma

# --- КАТЕГОРИИ ---
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название категории")
    slug = models.SlugField(unique=True) # Для красивых урлов
    icon = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

# --- АКЦИИ ---
class Promotion(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название акции")
    discount_percent = models.PositiveIntegerField(verbose_name="Процент скидки")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.discount_percent}%"

# --- ТОВАР ---
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    # ВОТ ТУТ МЫ ПРИВЯЗАЛИ ТВОЮ ФИРМУ ИЗ ДРУГОЙ ПАПКИ:
    firma = models.ForeignKey(Firma, on_delete=models.SET_NULL, null=True, blank=True)

    name = models.CharField(max_length=255, verbose_name="Название товара")
    article = models.CharField(max_length=50, unique=True, verbose_name="Артикул")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=0, verbose_name="Остаток на складе")

    def __str__(self):
        return self.name

class NewImage(models.Model):
    image = models.ImageField(upload_to='new_product_images')
    new_image = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

# --- ОТЗЫВЫ ---
class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')

    # Связываем с твоим кастомным юзером через settings (так советует дока Django)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} -> {self.product.name}"

# --- ИЗБРАННОЕ
class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product') # чтоб юзер не добавил один товар дважды

# СРАВНЕНИЕ ---
class Compare(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comparisons')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

# --- КОРЗИНА ---
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

# --- ЗАКАЗ ---
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='В обработке')
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    address = models.CharField(max_length=255, verbose_name="Адрес доставки")

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Сохраняем цену, которая была на момент покупки
    quantity = models.PositiveIntegerField()

# --- НОВОСТИ И КОНТАКТЫ ---
class News(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)




