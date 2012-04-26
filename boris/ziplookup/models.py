from django.db import models
from django.contrib.localflavor.us import models as us_models

class ZipCode(models.Model):
    zipcode = models.CharField(max_length=10,db_index=True)
    city = models.CharField(max_length=255)
    state = us_models.USPostalCodeField()
    
    def __unicode__(self):
        return self.zipcode