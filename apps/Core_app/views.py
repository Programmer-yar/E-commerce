from django.shortcuts import render
from apps.store.models import Product

def frontpage(request):
    all_products = Product.objects.filter(is_featured=True)
    context = {
    'products': all_products
    }
    return render(request, 'frontpage.html', context)

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')
