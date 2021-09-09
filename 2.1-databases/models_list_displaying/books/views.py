from django.shortcuts import render, redirect
from books.models import Book

all_dates = []
for book in Book.objects.all().order_by('-pub_date'):
    if book.pub_date not in all_dates:
        all_dates.append(book.pub_date)

class Page:
    def __init__(self, next_page, previous_page):
        self.next_page = next_page
        self.has_next = (next_page is not None)
        self.previous_page = previous_page
        self.has_previous = (previous_page is not None)

def index(request):
    return redirect('books')

def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all().order_by('pub_date')
    context = {'books': books}
    return render(request, template, context)

def show_by_date(request, slug):
    template = 'books/books_list.html'
    books = Book.objects.filter(pub_date=slug)
    current_date_index = all_dates.index(books[0].pub_date)
    previous_date = None
    next_date = None
    if current_date_index > 0:
        previous_date = all_dates[current_date_index - 1].strftime('%Y-%m-%d')
    if current_date_index < len(all_dates) - 1:
        next_date = all_dates[current_date_index + 1].strftime('%Y-%m-%d')
    page = Page(previous_date, next_date)
    context = {'books': books,
               'page': page}
    return render(request, template, context)
