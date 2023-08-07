from django.db import models
from apps.account import User
# Create your models here.


# Model for Category
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    class Meta:
        related_name = 'Категория'
        related_name_plural = 'Категорий'

    def __str__(self):
        return self.name

# Model for Product
class Product(models.Model):
    title = models.CharField(max_length=200, null=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    stock_count = models.IntegerField()
    category = models.ForeignKey(
        Category, 
        verbose_name="Категория",
        on_delete=models.PROTECT,
        related_name="products"
        )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ["-created_at"]


    def __str__(self):
        return self.title

# Model for Product Image
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField()
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.title}"

# Model for Order
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.IntegerField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.login}"

# Model for Order Item
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.title} in Order #{self.order.id}"
