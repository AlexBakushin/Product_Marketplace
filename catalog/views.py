from django.shortcuts import render
from catalog.models import Product


def product(request, pk):
    product_pk_name = Product.objects.get(pk=pk)
    product_name = str(product_pk_name)[2:].title()
    context = {
            'title': product_name,
            'object': Product.objects.get(pk=pk)
        }
    return render(request, 'catalog/product.html', context)


def home(request):
    product_list = Product.objects.all()
    context = {
        'title': 'Главная',
        'object_list': product_list
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    context = {
        'title': 'Контакты'
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя: {name}\nТелефон: {phone}\nСообщение: {message}')
    return render(request, 'catalog/contacts.html', context)
