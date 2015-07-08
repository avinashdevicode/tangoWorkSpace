from django.shortcuts import render
from django.http import HttpResponse

def index(request):
  context_dict = {'message':"hey i am the message"}
  return render(request, 'rango/index.html', context_dict) 
  
def about(request):
  return HttpResponse("<html><body>its a about page<br><a href='/rango/'>home</a></br></body></html>") 