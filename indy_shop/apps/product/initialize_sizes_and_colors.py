# apps/your_app/management/commands/initialize_sizes_and_colors.py
from django.core.management.base import BaseCommand
from apps.product.models import Size, Color

SIZE_CHOICES = [
    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
]

COLOR_CHOICES = [
    ('коричневый', 'Коричневый'),
    ('желтый', 'Желтый'),
    ('черный', 'Черный'),
    ('красный', 'Красный'),
    ('синий', 'Синий'),
    ('зеленый', 'Зеленый'),
    ('розовый', 'Розовый'),
    ('белый', 'Белый'),
]

class Command(BaseCommand):
    help = 'Initialize default sizes and colors'

    def handle(self, *args, **kwargs):
        # Проверяем, есть ли уже размеры и цвета в базе данных
        if not Size.objects.exists():
            # Добавляем размеры
            for size_code, size_name in SIZE_CHOICES:
                Size.objects.create(name=size_name)

        if not Color.objects.exists():
            # Добавляем цвета
            for color_code, color_name in COLOR_CHOICES:
                Color.objects.create(name=color_name)

        self.stdout.write(self.style.SUCCESS('Successfully initialized sizes and colors'))
