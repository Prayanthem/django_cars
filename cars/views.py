from django.http import HttpResponse, Http404
from .models import Car
from django.shortcuts import render, get_object_or_404, render_to_response
from .analysis import MyAnalysis
from django.forms.models import model_to_dict
from .forms import SearchForm, PriceCalculatorForm
import json
from django.template import RequestContext
from django.views.generic.list import ListView
from django.utils import timezone
from django.core.paginator import Paginator
import numpy as np

'''
    Static Views
'''
def methodology(request):
    return render(request, 'cars/methodology.html')

def contact_us(request):
    return render(request, 'cars/contact.html')

def about_us(request):
    return render(request, 'cars/about.html')

def howto(request):
    return render(request, 'cars/how_to.html')

def legal(request):
    return render(request, 'cars/legal.html')

'''
    Generic Views
'''
class CarListView(ListView):
    model = Car
    template_name = 'cars/car_list.html'
    car_list = Car.objects.all().order_by('-age')
    queryset = car_list
    context_object_name = "car_list"   
    paginate_by = 25 

class ModelListView(ListView):
    model = Car
    template_name = 'cars/model_list.html'  
    paginate_by = 25
    model_list = Car.objects.distinct('name')
    queryset = model_list
    context_object_name = 'model_list'

    def get_context_data(self,**kwargs):
        context = super(ModelListView,self).get_context_data(**kwargs)
        return context

class CategoryListView(ListView):
    model = Car
    template_name = 'cars/category_list.html'  
    paginate_by = 25
    model_list = Car.objects.distinct('Karosseri')
    queryset = model_list
    context_object_name = 'model_list'



'''
    Custom Views
'''
def index(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data['model']
            return model_statistics(request, name)
    else:
        form = SearchForm()

    model_list = list(Car.objects.distinct('name').only('name')) #check performance with and without only
    category_list = list(Car.objects.distinct('Karosseri').only('Karosseri')) #check performance with and without only
    context = {
        'form' : form,
        'model_list' : model_list,
        'category_list' : category_list,
    }
    return render(request, "cars/index.html", context)

def detail(request, finn_kode):
    anal = MyAnalysis()

    car = get_object_or_404(Car, Finn_kode=finn_kode)
    ser_car = model_to_dict(car)
    price_history = anal.graph_price_history(finn_kode)
    return render(request, "cars/detail.html", {
        'car' : car,
        'ser_car' : ser_car,
        'chart' : price_history,
    })

def display_data(request):
    anal = MyAnalysis()
    df = anal.get_dataframe().to_html
    return render(request, 'cars/data.html', {
        'df' : df,
    })

def model_statistics(request, car_name):
    anal = MyAnalysis()

    df = anal.get_dataframe_by_name(car_name).sort_values('Kmstand')
    model = anal.get_model(df)
    summary = anal.get_summary(model)
    chart = anal.graph_model_interactive(df, model)

    return render(request, 'cars/statistics.html', {
        'chart' : chart,
        'df' : df.to_html,
        'summary' : summary,
    })

def karosseri_statistics(request, karosseri):
    anal = MyAnalysis()

    df = anal.get_dataframe_by_karosseri(karosseri)
    model = anal.get_model(df, formula='np.log(pris) ~ Kmstand + C(name, Treatment) + Årsmodell')
    summary = anal.get_summary(model)
    chart = None#anal.graph_model_interactive(df, model)

    return render(request, 'cars/statistics.html', {
        'chart' : chart,
        'df' : df.to_html,
        'summary' : summary,
    })

#Todo: Price trends? Need bigger DB
def price_calculator(request):
    anal = MyAnalysis()
    estimated_price = "Estimated Price"
    summary = None
    conf_int = None
    if request.method == 'GET':
        form = PriceCalculatorForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data['model']
            km = form.cleaned_data['km']
            if form.cleaned_data['year']:
                year = form.cleaned_data['year']
                df = anal.get_dataframe_by_name(name)
                model = anal.get_model(df, formula="np.log(pris) ~ Kmstand + Årsmodell")
                equation = anal.get_equation(model)
                estimated_price = np.exp(equation['Intercept'] + km*equation['Kmstand'] + year*equation['Årsmodell'])
                estimated_price = "{:.0f} NOK".format(estimated_price)
                summary = anal.get_summary(model)
            else:
                df = anal.get_dataframe_by_name(name)
                model = anal.get_model(df)
                equation = anal.get_equation(model)
                estimated_price = np.exp(equation['Intercept'] + km*equation['Kmstand'])
                estimated_price = "{:.0f} NOK".format(estimated_price)
                summary = anal.get_summary(model)
        else:
            print("Form is not valid.")
    else:
        form = PriceCalculatorForm()

    car_list = list(Car.objects.distinct('name'))
    context = {
        'form' : form,
        'estimated_price' : estimated_price,
        'summary' : summary,
        'conf_int' : conf_int,
    }
    return render(request, "cars/price_calc.html", context)