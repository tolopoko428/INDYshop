from django.db import models
from apps.account.models import User
from django.core.validators import MaxValueValidator
# Create your models here.
SIZE_CHOICES = [
    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
]

COLOR_CHOICES = [
    ('коричневый', 'Коричневый'),
    ('желтый', 'Желтый'),
    ('черный', 'Черный'),
    ('красный', 'Красный'),
    ('синий', 'Синий'),
    ('зеленый', 'Зеленый'),
    ('розовый', 'Розовый'),
    ('белый', 'Белый'),
]

# Model for Category
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name



class Product(models.Model):
    STATUS_CHOICES = [
        ('in_stock', 'In Stock'),
        ('out_of_stock', 'Out of Stock'),
    ]

    title = models.CharField(max_length=200, null=False)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    stock_count = models.IntegerField(blank=True, null=True)
    is_new = models.BooleanField(default=False)
    is_top = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    rating = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)])
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_stock')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    @property
    def get_image(self):
        images = self.image.all()
        print(images)
        if images:
            images = list(images)
            return images[0].image.url
        return ""

    

# Model for Product Image
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="image")
    image = models.ImageField("Изображение",upload_to="products/images/" , null=True,blank=True ) 
    is_main = models.BooleanField("Главное изображение", default=False)

    class Meta:
        verbose_name = 'Изображения'
        verbose_name_plural = 'Изображений'



# Model for Order
class Orders(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total_amount = models.IntegerField()
    status = models.CharField(max_length=20, choices=[
        ('Обработка', 'Обработка'),
        ('В пути', 'В пути'),
        ('Доставлено', 'Доставлено')
    ], default='Обработка')
    created_at = models.DateTimeField(auto_now_add=True)
    postal_code = models.CharField(max_length=10, null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} by {self.user_id.email}"




# Model for Order Item
class OrderItem(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='order_items')
    order_item_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Эдемент Заказа'
        verbose_name_plural = 'Эдементы Заказов'
        ordering = ['-update_at']


    def __str__(self):
        return f"{self.order_item_id} in Order #{self.order_id.id}"

    

class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Изюранный'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return f"{self.product.title} в избранном у {self.user.email}"
    

    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('Product', through='CartItem')

    class Meta:
        verbose_name = 'Карзина'
        verbose_name_plural = 'Товары в Корзине'




class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Элемент Карзина'
        verbose_name_plural = 'Элементы Корзины'

    def get_total_price(self):
        return self.product.price * self.quantity

    def save(self, *args, **kwargs):
        self.total = self.get_total_price()
        super(CartItem, self).save(*args, **kwargs)

    

class Size(models.Model):
    name = models.CharField(max_length=5, choices=SIZE_CHOICES)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=10, choices=COLOR_CHOICES)

    def __str__(self):
        return self.name

