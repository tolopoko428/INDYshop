# Generated by Django 4.2.4 on 2023-10-04 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0040_orderhistory'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderHistory',
        ),
    ]