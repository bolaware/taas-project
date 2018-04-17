# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app.models import Measurement,FabricCollection,Ratings,Designer,Styles,Country,Accessories,Fabrics,Profile,Category,Transactions,Order

class DesignerAdmin(admin.ModelAdmin):
    model = Designer
    list_display = ('name', 'user','average_rating','dp','cover_photo','city','country','address')
    
class RatingsAdmin(admin.ModelAdmin):
    model = Ratings
    list_display = ('comment', 'rating','designer','user')
    
class StylesAdmin(admin.ModelAdmin):
    model = Styles
    list_display = ('code','name','designer','custom_price','gender','pub_date')
    
class CountryAdmin(admin.ModelAdmin):
    model = Styles
    list_display = ('name',)
    
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display=('name',)
    
class AccessoriesAdmin(admin.ModelAdmin):
    model = Accessories
    list_display = ('name','price','designer','gender')
    
class FabricsAdmin(admin.ModelAdmin):
    model=Fabrics
    list_display = ('name','price','designer')
    
class ProfileAdmin(admin.ModelAdmin):
    model=Profile
    list_display = ('user','city','country','address')
    
class TransactionsAdmin(admin.ModelAdmin):
    model=Transactions
    list_display = ('user','reference','amount','status')

class FabricCollectionAdmin(admin.ModelAdmin):
    model=FabricCollection
    list_display = ('name','designer',)    

class OrdersAdmin(admin.ModelAdmin):
    model=Transactions
    list_display = ('user','designer','style','fabric','transaction','reference')
    
class MeasurementAdmin(admin.ModelAdmin):
    model=Measurement
    
admin.site.register(Designer,DesignerAdmin)
admin.site.register(Ratings,RatingsAdmin)
admin.site.register(Styles,StylesAdmin)
admin.site.register(Country,CountryAdmin)
admin.site.register(Accessories,AccessoriesAdmin)
admin.site.register(Fabrics,FabricsAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Transactions,TransactionsAdmin)
admin.site.register(Order,OrdersAdmin)
admin.site.register(Measurement,MeasurementAdmin)
admin.site.register(FabricCollection,FabricCollectionAdmin)


