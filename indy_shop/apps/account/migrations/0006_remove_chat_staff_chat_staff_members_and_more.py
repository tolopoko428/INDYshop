# Generated by Django 4.2.4 on 2023-10-05 06:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_chat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='staff',
        ),
        migrations.AddField(
            model_name='chat',
            name='staff_members',
            field=models.ManyToManyField(related_name='staff_chats', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]