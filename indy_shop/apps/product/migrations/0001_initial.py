# Generated by Django 4.2.4 on 2023-08-25 01:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категорий',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('stock_count', models.IntegerField()),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='product.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('is_main', models.BooleanField(default=False)),
                ('product_image_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.IntegerField()),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='product.orders')),
                ('order_item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='product.product')),
            ],
        ),
    ]
