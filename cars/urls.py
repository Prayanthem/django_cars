from django.contrib import admin
from django.urls import include, path, re_path
from . import views

app_name = 'cars'
urlpatterns = [
    # ex: /cars/
    path('', views.index, name='index'),
    # ex: /cars/methodology/
    path('methodology/', views.methodology, name='methodology'),
    # ex: /cars/methodology/
    path('contact/', views.contact, name='contact'),
    # ex: /cars/methodology/
    path('howto/', views.howto, name='howto'),
    # ex: /cars/price/
    path('price/', views.price_calculator, name='price_calculator'),
    # ex: /cars/Audi+A5
    path('<str:car_name>/', views.statistics, name='statistics'),
    # ex: /cars/Audi+A5/1039383
    re_path(r'(?P<finn_kode>\d+)/?$', views.detail, name='detail'), #I dont think this is an optimal pattern
]
