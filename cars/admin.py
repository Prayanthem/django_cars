from django.contrib import admin
from .models import Car
from .models import Price

# Register your models here.
admin.site.register(Car)
admin.site.register(Price)
