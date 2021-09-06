from django.http import HttpResponse
from django.shortcuts import render, reverse
import os
from datetime import datetime


def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }

    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    # возвращает текущее время
    dt = datetime.now()
    current_time = dt.strftime("%A, %d. %B %Y %H:%M:%S")
    msg = f'Current time:<br>{current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    # возвращает список файлов в рабочей
    # директории
    files_list = 'Current directory:<br><ul type="square">' + \
                 ''.join([f'<li>{item}</li>' for item in os.listdir()])
    return HttpResponse(files_list)