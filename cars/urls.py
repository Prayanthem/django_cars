from django.contrib import admin
from django.urls import include, path, re_path
from . import views
from cars.views import CarListView, ModelListView

app_name = 'cars'
urlpatterns = [
    # ex: /cars/
    path('', views.index, name='index'),
    # ex: /cars/car/
    path('car/', CarListView.as_view(), name='car_list'),
    # ex: /cars/model/
    path('model/', ModelListView.as_view(), name='model_list'),
    # ex: /cars/methodology/
    path('methodology/', views.methodology, name='methodology'),
    # ex: /cars/contact/
    path('contact/', views.contact, name='contact'),
    # ex: /cars/howto/
    path('howto/', views.howto, name='howto'),
    # ex: /cars/legal/
    path('legal/', views.legal, name='legal'),
    # ex: /cars/price/
    path('price/', views.price_calculator, name='price_calculator'),
    # ex: /cars/data/
    path('data/', views.display_data, name='display_data'),
    # ex: /cars/model/Audi+A5
    path('categories/<str:karosseri>/', views.karosseri_statistics, name='karosseri_statistics'),
    # ex: /cars/type/SUV
    path('model/<str:car_name>/', views.model_statistics, name='model_statistics'),
    # ex: /cars/Audi+A5/1039383
    re_path(r'car/(?P<finn_kode>\d+)/', views.detail, name='detail'), #I dont think this is an optimal pattern
]
