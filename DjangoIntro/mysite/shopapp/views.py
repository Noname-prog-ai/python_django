from django.shortcuts import render

# Create your views here.
from django.utils import timezone

def index(request):
    context = {
        'title': 'Добро пожаловать в магазин',
        'description': 'Этот магазин предлагает множество товаров.',
        'now': timezone.now(),
    }
    return render(request, 'shopapp/index.html', context)