from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^category/(?P<category_slug>[\w\-]+)/$', views.category, name='category'),
                       url(r'^add_category/$', views.add_category, name="add_category"),
                       url(r'^register/', views.register, name="register"),
                       url(r'^category/(?P<category_slug>[\w\-]+)/add_page/$', views.add_page, name="add_page"),
                       url(r'login/', views.user_login, name='user_login'),
                       url(r'^logout/', views.user_logout, name='user_logout'),
                       url(r'^about/',views.about, name='about'))