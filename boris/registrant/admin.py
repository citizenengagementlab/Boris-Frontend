from registrant.models import *
from django.contrib import admin

def ignore_registrant(modeladmin, request, queryset):
    queryset.update(ignore=True)
ignore_registrant.short_description = "Ignore this registrant in summary stats"

def unignore_registrant(modeladmin, request, queryset):
    queryset.update(ignore=False)
unignore_registrant.short_description = "Don't ignore this registrant in summary stats"

class RegistrantAdmin(admin.ModelAdmin):
    list_display = ['email','first_name','last_name','created_at','zip_code','num_fields','ignore']
    actions = [ignore_registrant,unignore_registrant]

class ProgressAdmin(admin.ModelAdmin):
    list_display = ['created_at','registrant','field_name','field_value']
    raw_id_fields = ['registrant',]
    

admin.site.register(Registrant,RegistrantAdmin)
admin.site.register(RegistrationProgress,ProgressAdmin)