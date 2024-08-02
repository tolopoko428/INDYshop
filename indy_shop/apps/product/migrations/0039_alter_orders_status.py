# Generated by Django 4.2.4 on 2023-09-29 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0038_cartitem_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(choices=[('Новый Заказ', 'Новый Заказ'), ('Обработка', 'Обработка'), ('В пути', 'В пути'), ('Доставлено', 'Доставлено'), ('Отменен', 'Отменен')], default='Новый Заказ', max_length=20),
        ),
    ]