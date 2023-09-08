from django.db import models
from apps.account.models import User
# Create your models here.


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

#Model for Product
class Product(models.Model):
    title = models.CharField(max_length=200, null=False)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    stock_count = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    is_new = models.BooleanField(default=False)
    is_top = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', null=True, blank=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    

# Model for Product Image
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    images = models.ImageField()
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.title}"

# Model for Order
class Orders(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total_amount = models.IntegerField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.login}"

# Model for Order Item
class OrderItem(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='order_items')
    order_item_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField()
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.title} in Order #{self.order.id}"
