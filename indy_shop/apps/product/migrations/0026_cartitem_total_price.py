# Generated by Django 4.2.4 on 2023-09-25 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0025_orders_postal_code_alter_orders_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='total_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]