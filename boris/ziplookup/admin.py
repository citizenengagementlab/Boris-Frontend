from ziplookup.models import *
from django.contrib import admin

class ZipCodeAdmin(admin.ModelAdmin):
    list_display = ['zipcode','city','state']
    list_filter = ['state',]
    search_fields = ['zipcode','city']

admin.site.register(ZipCode,ZipCodeAdmin)