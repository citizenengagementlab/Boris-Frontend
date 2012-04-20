from django.db import models

class Registrant(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    zip_code = models.CharField(max_length=10)
    
    def __unicode__(self):
        return "%s %s" % (self.first_name,self.last_name)
    
    class Meta:
        ordering = ['created_at',]
        get_latest_by = 'created_at'
    
class RegistrationProgress(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    registrant = models.ForeignKey('Registrant')
    field_name = models.CharField(max_length=100)
    field_value = models.CharField(max_length=100)