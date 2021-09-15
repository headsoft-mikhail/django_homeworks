from django.views.generic import ListView
from django.shortcuts import render

from .models import Student, Teacher


def students_list(request):
    template = 'school/students_list.html'
    ordering = 'group'
    # students = Student.objects.order_by(ordering)  # по 1 запросу на каждого студента (дольше, сильнее нагружает БД)
    students = Student.objects.prefetch_related('teachers').order_by(ordering)  # всего 2 запроса
    context = {'object_list': students}

    return render(request, template, context)
