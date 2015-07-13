from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page, UserProfile
from forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate
from django.contrib.auth.views import login, logout
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import datetime


def my_login_required(function):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if not user.username:
            next = [request.path]
            print next
            return user_login(request, next)
        elif not user.is_active:
            return HttpResponse("Your account is disabled")
        else:
            return function(request, *args,**kwargs)
    return wrapper
            

def index(request):
    categories = Category.objects.order_by('-likes')[:5]
    pages = Page.objects.order_by("-views")[:5]
    context_dict = {'categories':categories, 'pages':pages}
    visits = request.session.get("visits")
    reset_last_vist_time_set = False
    response = render(request, 'rango/index.html', context_dict)
    print "---------number of visits ====" + str(visits)
    print "last visit ----------------" + str(request.session.get('last_visit'))
    if not visits:
        visits=1
    if "last_visit" in request.session:
        last_visit = request.session.get('last_visit')
        reset_last_vist_time_set = True
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        
        if (datetime.now()- last_visit_time).seconds >2:
            visits += 1
        context_dict['visits'] = visits
        response = render(request, 'rango/index.html', context_dict)    
    else:
        request.session["last_vist"] = str(datetime.now())
        request.session["visits"] = visits
        context_dict['visits'] = visits
        reset_last_vist_time_set = True
        response = render(request, 'rango/index.html', context_dict)
        
    if reset_last_vist_time_set:
        print "I am here ...................."
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    return response

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


@my_login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return index(request)
        else:
            print form.errors
            
    else:
        form = CategoryForm()
    return render(request, 'rango/add_category.html', {'form':form})

@my_login_required
def add_page(request, category_slug):
    context_dict = {}
    cat = Category.objects.get(slug=category_slug)
    context_dict['category'] = cat
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_slug)
        else:
            print form.errors
    else:
        form = PageForm()
        context_dict['form'] = form
        
    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    registerd = False
    context_dict = {}
    context_dict['registerd'] = registerd
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['pictures']
            profile.save()
            registerd = True
            context_dict['registerd'] = registerd
        else:
            print user_form.errors, profile_form.errors
    else:
        context_dict['user_form'] = UserForm
        context_dict['profile_form'] = UserProfileForm
    
    return render(request, 'rango/register.html', context_dict )

def user_login(request, *nexts):
    if request.method == 'POST':
        print nexts
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                print "I am here"
                print type(request)
                if request.POST.get('next'):
                    next = request.POST.get('next')
                    print next
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("your accound beeen disabled")
        else:
            print "Invalid credentioals {0}, {1}".format(username, password)
        
    else:
        return render(request, 'rango/login.html', {})
    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')
    































        