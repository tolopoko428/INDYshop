# Generated by Django 4.2.4 on 2023-09-05 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_product_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productimage',
            old_name='image',
            new_name='images',
        ),
    ]
