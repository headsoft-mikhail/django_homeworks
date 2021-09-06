from django.shortcuts import render, reverse
from django.http import HttpResponse

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    'borsch': {
        'свекла, шт.': 1,
        'морковь, шт.': 1,
        'луковица, шт.': 1,
        'катрофель, шт.': 3,
        'говядина, г': 200,
        'капуста, г': 100,
    }
}

def main_view(request):
    template_name = 'calculator/home.html'
    pages = {}
    for item in DATA.keys():
        pages[item] = reverse(item)
    context = {
        'pages': pages
    }
    return render(request, template_name, context)

def recipe_view(request):
    print(request)
    template_name = 'calculator/recipe.html'
    try:
        amount = int(request.GET.get('servings'))
        if amount < 0:
            amount = 1
    except TypeError:
        amount = 1
    context = {
        'recipe': {key: amount * value
                   for key, value in DATA[request.META.get('PATH_INFO').replace('/', '')].items()}
    }
    return render(request, template_name, context)

