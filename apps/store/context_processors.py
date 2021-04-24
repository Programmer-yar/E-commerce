from .models import Category

def menu_categories_func(request):
    categories = Category.objects.all()

    return { 'menu_categories':categories }