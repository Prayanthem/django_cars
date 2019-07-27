from django import forms
from django.core.exceptions import ValidationError
from .models import Car
from django.utils.translation import ugettext_lazy as _

class SearchForm(forms.Form):
    model = forms.CharField(widget=forms.TextInput(attrs={
        'type':'search', 
        'class' : 'search-box is-size-3-desktop', 
        'placeholder' : 'Search for a car model',
        }))

    def clean_model(self):
        data = self.cleaned_data['model']
        ##FIx a check for if mdoel in modelnames
        #if data not in Car.objects.order_by('name').values().distinct():
        #    raise ValidationError(_('Invalid model name - model name doesn\'t exist'))
        return data

class PriceCalculatorForm(forms.Form):
    model = forms.CharField(widget=forms.TextInput(attrs={
        'type' : 'text',
        'class' : 'input is-medium',
        'placeholder':'Name of car model',
        'order' : '1'
    }))

    km = forms.IntegerField(widget=forms.TextInput(attrs={
        'type' : 'text',
        'class' : 'input is-medium',
        'placeholder':'Number of kilometers ran',
        'order' : '2',
    }))

    year = forms.IntegerField(required=False, widget=forms.TextInput(attrs={
        'type' : 'text',
        'class' : 'input is-medium',
        'placeholder':'Model Year',
        'order' : '3',
    }))

    def clean_km(self):
        data = self.cleaned_data['km']
        if not isinstance(data, int):
            raise ValidationError(_('Invalid KM - KM is not an Integer'))
        return data
    def clean_model(self):
        data = self.cleaned_data['model']
        ##FIx a check for if mdoel in modelnames
        if r'[^A-Za-z0-9]' in data:
            raise ValidationError(_('Invalid model name - model contains illegal characters'))
        return data
    def clean_year(self):
        data = self.cleaned_data['year']
        return data

