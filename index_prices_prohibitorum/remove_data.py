import os, sys
import django

if __name__ == "__main__":
    # https://stackoverflow.com/questions/22744949/runtime-errorapp-registry-isnt-ready-yet/23241093#23241093
    path = 'C:/Users/taplop/Code/django_cars'  # use your own username here
    if path not in sys.path:
        sys.path.append(path)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'index_prices_prohibitorum.settings')
    django.setup()
    from cars.models import Car
    cars = Car.objects.filter(pk__in=Car.objects.all().values_list('Finn_kode')[2450:])
    print(cars.count())
    cars.delete()
    print(Car.objects.all().count())

