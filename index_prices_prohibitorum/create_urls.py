import os, sys
import django

if __name__ == "__main__":
    print("Starting...")
    # https://stackoverflow.com/questions/22744949/runtime-errorapp-registry-isnt-ready-yet/23241093#23241093
    path = 'C:/Users/taplop/Code/django_cars'  # use your own username here
    if path not in sys.path:
        sys.path.append(path)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'index_prices_prohibitorum.settings')
    django.setup()
    base_url = 'https://www.finn.no/car/used/ad.html?finnkode='
    from index_prices_prohibitorum import settings
    print(settings.DATABASES)
    from cars.models import Car
    my_file = open('urls.txt', 'w')
    if not Car.objects.all():
        print("No cars found.")
    for car in Car.objects.filter(solgt=False):
        url = 'https://www.finn.no/car/used/ad.html?finnkode={}\n'.format(car.Finn_kode)
        my_file.write(url)
    my_file.close()