# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app.models import Ratings,Designer,Styles,Country,Accessories,Fabrics,Profile

class DesignerAdmin(admin.ModelAdmin):
    model = Designer
    list_display = ('name', 'user','average_rating','dp','cover_photo','city','country','address')
    
class RatingsAdmin(admin.ModelAdmin):
    model = Ratings
    list_display = ('comment', 'rating','designer')
    
class StylesAdmin(admin.ModelAdmin):
    model = Styles
    list_display = ('name','designer','service_price','custom_price','sale_format','gender','pub_date')
    
class CountryAdmin(admin.ModelAdmin):
    model = Styles
    list_display = ('name',)
    
class AccessoriesAdmin(admin.ModelAdmin):
    model = Accessories
    list_display = ('name','price','designer','gender')
    
class FabricsAdmin(admin.ModelAdmin):
    model=Fabrics
    list_display = ('name','price','designer')
    
class ProfileAdmin(admin.ModelAdmin):
    model=Profile
    list_display = ('user','city','country','address')
    

admin.site.register(Designer,DesignerAdmin)
admin.site.register(Ratings,RatingsAdmin)
admin.site.register(Styles,StylesAdmin)
admin.site.register(Country,CountryAdmin)
admin.site.register(Accessories,AccessoriesAdmin)
admin.site.register(Fabrics,FabricsAdmin)
admin.site.register(Profile,ProfileAdmin)


