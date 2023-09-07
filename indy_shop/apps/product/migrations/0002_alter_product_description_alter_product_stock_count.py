# Generated by Django 4.2.4 on 2023-09-05 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
