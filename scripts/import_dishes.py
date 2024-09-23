import json
import os
import sys

import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject3.settings')
django.setup()

from kitchen.models import Dish, DishType


def load_dishes_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        dishes = json.load(file)
        for dish_data in dishes:
            # Отримуємо або створюємо DishType
            dish_type, created = DishType.objects.get_or_create(name=dish_data['dish_type'])
            dish_data['dish_type'] = dish_type  # Призначаємо екземпляр DishType

            # Створюємо Dish
            Dish.objects.create(**dish_data)
    print("Дані успішно імпортовані!")


if __name__ == '__main__':
    load_dishes_from_json(os.path.join(os.path.dirname(__file__), 'dishes.json'))
