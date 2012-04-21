from registrant.models import *
from django.contrib import admin

class RegistrantAdmin(admin.ModelAdmin):
    list_display = ['email','first_name','last_name','created_at','zip_code']

class ProgressAdmin(admin.ModelAdmin):
    list_display = ['created_at','registrant','field_name','field_value']

admin.site.register(Registrant,RegistrantAdmin)
admin.site.register(RegistrationProgress,ProgressAdmin)