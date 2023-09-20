# Generated by Django 4.2.4 on 2023-09-19 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_alter_cart_options_alter_cartitem_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')], max_length=5, null=True)),
                ('color', models.CharField(blank=True, choices=[('коричневый', 'Коричневый'), ('желтый', 'Желтый'), ('черный', 'Черный'), ('красный', 'Красный'), ('синий', 'Синий'), ('зеленый', 'Зеленый'), ('розовый', 'Розовый'), ('белый', 'Белый')], max_length=10, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'verbose_name': 'Вариант товара',
                'verbose_name_plural': 'Варианты товаров',
            },
        ),
    ]
