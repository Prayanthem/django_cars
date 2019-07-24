# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import date

class MycrawlerPipeline(object):
    def process_item(self, item, spider):
        print("Entering process_item method, and attempting to create a car object")
        # Importing models
        import sys
        import os
        import django
        path = 'C:/Users/taplop/Code/index_prices_prohibitorum'
        if path not in sys.path:
            sys.path.append(path)
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'index_prices_prohibitorum.settings')
        django.setup()

        # Creating model instances and saving them to DB
        from cars.models import Car, Price
        car = Car()
        car.Antalldører= item['Antalldører']
        car.Antalleiere= item['Antalleiere']
        car.Antallseter= item['Antallseter']
        car.Årsavgift = item['Årsavgift']
        car.Årsmodell= item['Årsmodell']
        car.Avgiftsklasse= item['Avgiftsklasse']
        car.Bilenståri= item['Bilenståri']
        car.ChassisnrVIN= item['ChassisnrVIN']
        car.CO2utslipp= item['CO2utslipp']
        car.Drivstoff= item['Drivstoff']
        car.Effekt= item['Effekt']
        car.Farge= item['Farge']
        car.Fargebeskrivelse= item['Fargebeskrivelse']
        car.foorstegangregistrert= item['foorstegangregistrert']
        car.Girkasse= item['Girkasse']
        car.header= item['header']
        car.Hjuldrift= item['Hjuldrift']
        car.Karosseri= item['Karosseri']
        car.Kmstand= item['Kmstand']
        car.last_updated = date.today()
        car.name= item['name']
        car.Omregistrering = item['Omregistrering']
        car.Priseksomreg = item['Priseksomreg']
        car.Regnr= item['Regnr']
        car.Salgsform= item['Salgsform']
        car.Sylindervolum= item['Sylindervolum']
        car.totalpris= item['totalpris']
        car.Vekt= item['Vekt']

        car.RekkeviddeWLTP = item['RekkeviddeWLTP']
        car.Batterikapasitet = item['Batterikapasitet']
        
        # Farger
        car.Interiørfarge = item['Interiørfarge']

        # Finn
        car.Finn_kode = item['Finn_kode']

        print(car)

        car.save()

        price = Price()
        price.date = date.today()
        price.price = item['totalpris']
        price.car = car

        price.save()

        return item

