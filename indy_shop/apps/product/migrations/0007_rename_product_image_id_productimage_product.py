# Generated by Django 4.2.4 on 2023-09-08 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_category_options_remove_product_category_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productimage',
            old_name='product_image_id',
            new_name='product',
        ),
    ]
