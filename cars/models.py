from django.db import models

# Create your models here.

class Car(models.Model):
    # General
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateField(blank=True, null=True,default=None)
    age=models.IntegerField(blank=True, null=True, default=0)
    name=models.TextField(blank=True, null=True, max_length=200,default=None)
    header=models.TextField(blank=True, null=True, default=0)
    Finn_kode = models.CharField(primary_key=True, blank=True, null=False, max_length=200)

    # From Scrapy
    #############

    #Strings
    Årsavgift = models.CharField(blank=True, null=True,max_length=200, default=None)
    Avgiftsklasse=models.CharField(blank=True, null=True,max_length=200,default=None)
    Bilenståri=models.CharField(blank=True, null=True,max_length=200,default=None)
    ChassisnrVIN=models.CharField(blank=True, null=True,max_length=200,default=None)
    Drivstoff=models.CharField(blank=True, null=True,max_length=200,default=None)
    Farge=models.CharField(blank=True, null=True,max_length=200,default=None)
    Fargebeskrivelse=models.CharField(blank=True, null=True,max_length=200,default=None)
    foorstegangregistrert=models.CharField(blank=True, null=True,max_length=200,default=None)
    Hjuldrift=models.CharField(blank=True, null=True,max_length=200,default=None)
    Karosseri=models.CharField(blank=True, null=True,max_length=200,default=None)
    Girkasse=models.CharField(blank=True, null=True,max_length=200,default=None)
    Regnr=models.CharField(blank=True, null=True,max_length=200,default=None)
    Salgsform=models.CharField(blank=True, null=True,max_length=200,default=None)
    Interiørfarge = models.CharField(blank=True, null=True, max_length=200)

    #Numericals
    Antalldører=models.IntegerField(blank=True, null=True, default=0)
    Antalleiere=models.IntegerField(blank=True, null=True, default=0)
    Antallseter=models.IntegerField(blank=True, null=True, default=0)
    Årsmodell=models.IntegerField(blank=True, null=True,default=0)
    CO2utslipp=models.IntegerField(blank=True, null=True, default=0)
    Effekt=models.IntegerField(blank=True, null=True, default=0)
    Kmstand=models.IntegerField(blank=True, null=True, default=0)
    Omregistrering = models.IntegerField(blank=True, null=True, default=0)
    Priseksomreg = models.IntegerField(blank=True, null=True, default=0)
    Sylindervolum=models.FloatField(blank=True, null=True, default=0)
    Vekt=models.IntegerField(blank=True, null=True, default=0)

    #Boolean
    solgt = models.BooleanField(default=False)

        # Elbil
    RekkeviddeWLTP = models.IntegerField(blank=True, null=True, default=0)
    Batterikapasitet = models.IntegerField(blank=True, null=True, default=0)
    

    def __str__(self):
        return self.name

class Price(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.IntegerField(default=0)