import json

from django.core.management.base import BaseCommand
from books.models import Book
from datetime import datetime

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('fixtures/books.json', 'r', encoding='utf-8') as file:
            books = json.load(file)
        for book in books:
            b = Book(name=book['fields']['name'],
                     author=book['fields']['author'],
                     pub_date=datetime.strptime(book['fields']['pub_date'], '%Y-%m-%d'))
            b.save()
