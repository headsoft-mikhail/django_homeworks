from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
import csv
import math
from pagination.settings import BUS_STATION_CSV as CSV_PATH

class Station():
    def __init__(self, name, street, district):
        self.Name = name
        self.Street = street
        self.District = district

items_per_page = 10
with open(CSV_PATH, newline='', encoding='utf8') as csvfile:
    reader = csv.DictReader(csvfile)
    stations = [Station(row['Name'], row['Street'], row['District']) for row in reader]
print('CSV data loaded')

def index(request):
    return redirect(reverse('bus_stations'))

def bus_stations(request):
    paginator = Paginator(stations, items_per_page)
    try:
        page_number = int(request.GET.get('page'))
        if page_number > len(stations)/items_per_page:
            page_number = math.ceil(len(stations)/items_per_page)
        if page_number <= 0:
            page_number = 1
    except TypeError:
        page_number = 1
    context = {
        'bus_stations': stations[(page_number-1)*items_per_page:page_number*items_per_page],
        'page': paginator.get_page(page_number),
    }
    return render(request, 'stations/index.html', context)
