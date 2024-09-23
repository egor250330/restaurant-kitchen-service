import json
import os
import sys

import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject3.settings')
django.setup()

from kitchen.models import Cook


def load_cooks_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        cooks = json.load(file)
        for cook_data in cooks:
            Cook.objects.create(**cook_data)
    print("Дані успішно імпортовані!")


if __name__ == '__main__':
    load_cooks_from_json(os.path.join(os.path.dirname(__file__), 'cooks.json'))
