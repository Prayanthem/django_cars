# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MycrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
    
class CarItem(scrapy.Item):
    last_updated = scrapy.Field(serializer=str)
    Omregistrering = scrapy.Field()
    Priseksomreg = scrapy.Field()
    Årsavgift = scrapy.Field()
    Årsmodell = scrapy.Field()
    foorstegangregistrert = scrapy.Field()
    Kmstand = scrapy.Field()
    Farge = scrapy.Field()
    Girkasse = scrapy.Field()
    Hjuldrift = scrapy.Field()
    Drivstoff = scrapy.Field()
    Effekt = scrapy.Field()
    Sylindervolum = scrapy.Field()
    Vekt = scrapy.Field()
    CO2utslipp = scrapy.Field()
    Antallseter = scrapy.Field()
    Karosseri = scrapy.Field()
    Antalldører = scrapy.Field()
    Antalleiere = scrapy.Field()
    Bilenståri = scrapy.Field()
    Salgsform = scrapy.Field()
    Avgiftsklasse = scrapy.Field()
    Regnr = scrapy.Field()
    ChassisnrVIN = scrapy.Field()
    name = scrapy.Field()
    header = scrapy.Field()
    totalpris = scrapy.Field()
    Fargebeskrivelse = scrapy.Field()

    Finn_kode = scrapy.Field()
    Batterikapasitet = scrapy.Field()
    RekkeviddeWLTP = scrapy.Field()
    Interiørfarge = scrapy.Field()

    def __repr__(self):
        """only print out Finn_kode after exiting the Pipeline"""
        return repr({"Finn_kode": self['Finn_kode']})