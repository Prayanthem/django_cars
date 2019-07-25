from django.http import HttpResponse, Http404
from .models import Car
from django.shortcuts import render, get_object_or_404
from .analysis import MyAnalysis as analysis
from django.forms.models import model_to_dict
from .forms import SearchForm, PriceCalculatorForm
import json

def index(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data['model']
            return statistics(request, name)
    else:
        form = SearchForm()

    car_list = list(Car.objects.distinct('name').only('name')) #check performance with and without only
    context = {
        'form' : form,
        'car_list' : car_list,
    }
    return render(request, "cars/index.html", context)

def detail(request, finn_kode):
    car = get_object_or_404(Car, Finn_kode=finn_kode)
    ser_car = model_to_dict(Car.objects.get(Finn_kode=finn_kode))
    return render(request, "cars/detail.html", {
        'car' : car,
        'ser_car' : ser_car,
    })

def methodology(request):
    return render(request, 'cars/methodology.html')

def contact(request):
    return render(request, 'cars/contact.html')

def howto(request):
    return render(request, 'cars/how_to.html')

def legal(request):
    return render(request, 'cars/legal.html')

def statistics(request, car_name):
    anal = analysis()

    df = anal.get_dataframe_django(car_name)
    model = anal.get_model(car_name)
    summary = anal.get_summary(model)
    chart = anal.graph_model_interactive(df, model)

    return render(request, 'cars/statistics.html', {
        'chart' : chart,
        'df' : df.to_html,
        'summary' : summary,
    })

def price_calculator(request):
    anal = analysis()
    estimated_price = "Estimated Price"
    summary = None
    conf_int = None
    if request.method == 'GET':
        form = PriceCalculatorForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data['model']
            km = form.cleaned_data['km']
            model = anal.get_model(name)
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