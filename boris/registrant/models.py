from django.db import models

LAYOUT_CHOICES = (('singlepage','singlepage'),
                  ('tabs','tabs'),
                  ('accordion','accordion'))

class Registrant(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100,blank=True,null=True)
    last_name = models.CharField(max_length=100,blank=True,null=True)
    email = models.EmailField()
    zip_code = models.CharField(max_length=10)
    layout = models.CharField(choices=LAYOUT_CHOICES,max_length=10)
    ignore = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s" % (self.email)
    
    def num_fields(self):
        return RegistrationProgress.objects.filter(registrant=self).count()
        
    def last_field(self):
        RegistrationProgress.objects.filter(registrant=self).latest().field_name
    
    class Meta:
        ordering = ['created_at',]
        get_latest_by = 'created_at'
    
class RegistrationProgress(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    registrant = models.ForeignKey('Registrant')
    field_name = models.CharField(max_length=100)
    field_value = models.CharField(max_length=100)
    
    class Meta:
        get_latest_by = 'created_at'
    
    def __unicode__(self):
        return "%s -> %s" % (self.registrant.email, self.field_name)