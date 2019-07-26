from django.http import HttpResponse, Http404
from .models import Car
from django.shortcuts import render, get_object_or_404
from .analysis import MyAnalysis
from django.forms.models import model_to_dict
from .forms import SearchForm, PriceCalculatorForm
import json

'''
    Static Views
'''
def methodology(request):
    return render(request, 'cars/methodology.html')

def contact(request):
    return render(request, 'cars/contact.html')

def howto(request):
    return render(request, 'cars/how_to.html')

def legal(request):
    return render(request, 'cars/legal.html')

'''
    Dynamic Views
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
    car = get_object_or_404(Car, Finn_kode=finn_kode)
    ser_car = model_to_dict(Car.objects.get(Finn_kode=finn_kode))
    return render(request, "cars/detail.html", {
        'car' : car,
        'ser_car' : ser_car,
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
    model = anal.get_model(df, formula='pris ~ Kmstand + C(name, Treatment) + Årsmodell')
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
            df = anal.get_dataframe_by_name(name)
            model = anal.get_model(df)
            equation = anal.get_equation(model)
            estimated_price = equation['intercept'] + km*equation['km']
            estimated_price = "{:.0f} NOK".format(estimated_price)
            summary = anal.get_summary(model)
            conf_int = model.conf_int(alpha=0.05, cols=None)
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