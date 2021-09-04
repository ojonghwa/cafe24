from django.db import models
#from django.core.validators import MinValueValidator, MaxValueValidator
#from decimal import Decimal


class Esp8266(models.Model):      
    espid = models.CharField(max_length=10)     #esp mr1 001 
    #temp = models.DecimalField(max_digits=3, decimal_places=2)
    #humi = models.DecimalField(max_digits=3, decimal_places=2)
    temp = models.CharField(max_length=6)
    humi = models.CharField(max_length=6)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

