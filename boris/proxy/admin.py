from proxy.models import *
from django.contrib import admin

class CustomFormAdmin(admin.ModelAdmin):
    list_display = ['name','partner_id']

admin.site.register(CustomForm,CustomFormAdmin)