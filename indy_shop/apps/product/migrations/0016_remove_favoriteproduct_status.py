# Generated by Django 4.2.4 on 2023-09-14 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_favoriteproduct_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favoriteproduct',
            name='status',
        ),
    ]
