from django.contrib import admin
from django.urls import include, path, re_path
from . import views

app_name = 'cars'
urlpatterns = [
    # ex: /cars/
    path('', views.index, name='index'),
    # ex: /cars/5/
    #path('<int:car_id>/', views.detail, name='detail'),
    # ex: /cars/5/results/
    path('<int:car_id>/results/', views.results, name='results'),
    # ex: /cars/price/
    path('price/', views.price_calculator, name='price_calculator'),
    # ex: /cars/Audi+A5
    path('<str:car_name>/', views.statistics, name='statistics'),
    # ex: /cars/Audi+A5/1039383
    re_path(r'(?P<finn_kode>\d+)/?$', views.detail, name='detail'), #I dont think this is an optimal pattern
]
