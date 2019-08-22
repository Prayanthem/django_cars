# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import CarItem
import json

class FinnBilSpider(scrapy.Spider):
    name = 'finn_bil'
    #allowed_domains = ['https://www.finn.no/car/used/search.html?filters=/']
    start_urls = ['https://www.finn.no/car/used/search.html?filters=/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'mycrawler.pipelines.FinnSecondhandPipeline': 400
        }
    }

    def parse(self, response):
        # follow links to cars
        for href in  response.css('a.ads__unit__link::attr(href)'):
            yield response.follow(href, self.parse_car_item)

        # follow pagination links
        next_page = response.xpath('//a[@rel="next"]').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_car(self, response):
        dicts = {}
        info_keys = response.css("dt::text").getall()
        info_values = response.css("dd::text").getall()
        refined_info_keys = []
        refined_info_values = []

        ### IDEA: 
        # Ta registreringsnummeret fra Finn og skrap heller vegvesen for mer utfyllende info
        # Hent ut bedre opplysninger, kontroller opplysninger, og pass på at km_finn > km_vegvesen.
        # https://www.vegvesen.no/kjoretoy/Kjop+og+salg/Kj%C3%B8ret%C3%B8yopplysninger?registreringsnummer=XXXXX

        #Remove special characters
        for k in info_keys:
            k.replace('\xa0', '')
            s = re.sub('[^A-Za-z0-9.]+', '', k)
            refined_info_keys.append(s)
        for v in info_values:
            v.replace('\xa0', '')
            s = re.sub(r'[^A-Za-z0-9.]+', '', v)
            s = re.sub(r'gkm$', '', s)
            s = re.sub(r'kr$', '', s)
            s = re.sub(r'km$', '', s)
            s = re.sub(r'Hk$', '', s)
            s = re.sub(r'kg$', '', s)
            s = re.sub(r'kWh$', '', s)
            refined_info_values.append(s)

        #Remove empty listentries
        refined_info_keys2 = [x.strip() for x in refined_info_keys if x.strip()]
        refined_info_values2 = [x.strip() for x in refined_info_values if x.strip()]

        #Add lists to dictionary - len(keys) > len(values) due to finnkodes.
        for i in range(0, len(refined_info_values2)):
            dicts[refined_info_keys2[i]] = refined_info_values2[i]

        ##ALSO STORE URL
        dicts['name'] = response.css('div.panel h1.u-t2::text')[0].get().replace('\xa0', ' ')
        dicts['header'] = response.css('div.panel h1.u-t2 + p::text')[0].get().replace('\xa0', ' ')
        dicts['totalpris'] = response.css('span.u-t3::text').get().replace('\xa0', '').replace(' kr', '')

        yield dicts
            
    def parse_car_item(self, response):
        dicts = {}
        info_keys = response.css("dt::text").getall()
        info_values = response.css("dd::text").getall()
        refined_info_keys = []
        refined_info_values = []

        #Remove special characters
        for k in info_keys:
            k.replace('\xa0', '')
            s = re.sub(r'[^A-Za-z0-9æøåÆØÅ]+', '', k)
            s = re.sub('-', '_', s)
            if s == '1gangregistrert':
                s = 'foorstegangregistrert'

            refined_info_keys.append(s)
        for v in info_values:
            v.replace('\xa0', '')
            s = re.sub(r'[^A-Za-z0-9.æøåÆØÅ]+', '', v)
            s = re.sub(r'gkm$', '', s)
            s = re.sub(r'kr$', '', s)
            s = re.sub(r'km$', '', s)
            s = re.sub(r'Hk$', '', s)
            s = re.sub(r'kg$', '', s)
            s = re.sub(r'\dl$', '', s)
            s = re.sub(r'\.$', '', s)
            s = re.sub(r'\.', '-', s)
            refined_info_values.append(s)
        #Remove empty listentries
        refined_info_keys2 = [x.strip() for x in refined_info_keys if x.strip()]
        refined_info_values2 = [x.strip() for x in refined_info_values if x.strip()]

        #Add lists to dictionary - len(keys) > len(values) due to finnkodes.
        for i in range(0, len(refined_info_values2)):
            dicts[refined_info_keys2[i]] = refined_info_values2[i]

        #print(json.dumps(dicts, indent=4))

        ##ALSO STORE URL
        dicts['name'] = s = re.sub(r"[^0-9a-zA-Z\n]", '', response.css('div.panel h1.u-t2::text')[0].get().replace('\xa0', ' '))
        dicts['header'] = response.css('div.panel h1.u-t2 + p::text')[0].get().replace('\xa0', ' ')
        dicts['totalpris'] = response.css('span.u-t3::text').get().replace('\xa0', '').replace(' kr', '')
        dicts['Finn_kode'] = str(response).split('=')[-1].replace('>', '')

        if "Omregistrering" in dicts:
            if dicts['Omregistrering'] == "Fritatt":
                dicts['Omregistrering'] = 0

        car_item = CarItem()
        for field in car_item.fields:
            if field in dicts:
                #print("%s successfully added to item" % field)
                car_item[field] = dicts[field]
            else:
                #print("%s key not in dicts! Setting NULL" % field)
                car_item[field] = None

        yield car_item