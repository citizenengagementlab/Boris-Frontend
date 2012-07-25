from proxy.models import *
from django.contrib import admin

class CustomFormAdmin(admin.ModelAdmin):
    list_display = ['name','partner_id']

class CoBrandFormAdmin(admin.ModelAdmin):
    list_display = ['name','partner_id','toplevel_org']


admin.site.register(CustomForm,CustomFormAdmin)
admin.site.register(CoBrandForm,CoBrandFormAdmin)