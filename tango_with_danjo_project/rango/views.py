from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page

def index(request):
    categories = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories':categories}
    return render(request, 'rango/index.html', context_dict)

def category(request, category_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category = category)
        context_dict['pages'] = pages
        context_dict['category'] = category
        
    except Category.doesNotExist:
        pass
    
    return render(request, 'rango/category.html', context_dict)
        
  
def about(request):
    context_dict = {'message':"this is about page hee"}
    return render(request, 'rango/about.html', context_dict) 