from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page

def index(request):
    categories = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories':categories}
    return render(request, 'rango/index.html', context_dict) 
  
def about(request):
    context_dict = {'message':"this is about page hee"}
    return render(request, 'rango/about.html', context_dict) 