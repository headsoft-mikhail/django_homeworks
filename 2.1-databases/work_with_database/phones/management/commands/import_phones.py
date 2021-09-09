import csv

from django.core.management.base import BaseCommand
from phones.models import Phone
from slugify import slugify
from datetime import datetime


def slug(name):
    return slugify(
        name.translate(
            str.maketrans(
                "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
                "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"
            )
        )
    )

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))
        for phone in phones:
            p = Phone(name=phone['name'],
                      price=phone['price'],
                      image=phone['image'],
                      release_date=datetime.strptime(phone['release_date'], '%Y-%m-%d'),
                      lte_exists=phone['lte_exists'],
                      slug=slug(phone['name']))
            p.save()





