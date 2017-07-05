# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        
class Country(models.Model):
    name=models.CharField(max_length=30)

    class Meta:
        ordering=["name"]

    def __str__(self):
        return self.name
        
def dp_file(instance,filename):
    name,ext=filename.split('.')
    filepath='dp/{name}.{ext}'.format(
        name=instance.name,ext=ext)
    return filepath  

def covers_file(instance,filename):
    name,ext=filename.split('.')
    filepath='cover_photo/{name}.{ext}'.format(
        name=instance.name,ext=ext)
    return filepath      

class Designer(models.Model):
    name=models.CharField(max_length=100)
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,editable=True)
    dp=models.ImageField(upload_to=dp_file)
    cover_photo=models.ImageField(upload_to=covers_file)
    city=models.CharField(max_length=15)
    country=models.ForeignKey(Country)
    address=models.TextField()
    
    @property
    def average_rating(self):
        avg=self.ratings_set.all().aggregate(models.Avg('rating'))['rating__avg']
        return avg
        
    @property
    def total_feeds(self):
        a=Authority.objects.get(id=self.id)
        return a.feed_set.all().count()
    
    
    def __str__(self):
        return self.name
        
class Ratings(models.Model):
    rating=models.DecimalField(max_digits=2,decimal_places=1)
    comment=models.TextField()
    designer=models.ForeignKey(Designer)
    def __str__(self):
        return self.comment
        
def fabrics_file(instance,filename):
    name,ext=filename.split('.')
    filepath='fabric_pic/{name}/{filename}'.format(
        name=instance.name,filename=filename)
    return filepath          
        

class Fabrics(models.Model):
    name=models.CharField(max_length=100)
    price=models.PositiveIntegerField()
    designer=models.ForeignKey(Designer,on_delete=models.CASCADE,related_name='fabrics')
    photo1=models.ImageField(upload_to=fabrics_file,blank=True,null=True)
    photo2=models.ImageField(upload_to=fabrics_file,blank=True,null=True)
     
    def __str__(self):
        return self.name
        
def styles_file(instance,filename):
    name,ext=filename.split('.')
    filepath='styles_pic/{designer}/{name}/{filename}'.format(
        designer=instance.designer.name,name=instance.name,filename=filename)
    return filepath  
        
class Styles(models.Model):
    SALE_FORMATS= (
        ('AS SHOWN', "Provide fabric as shown"),
        ('FABRIC CUSTOM', 'Provide custom fabric(s)'),
        ('BOTH', 'Both'),
    )
    GENDER=(
        ('M', "Male"),
        ('F', 'Female'),
    )
    name=models.CharField(max_length=100)
    designer=models.ForeignKey(Designer,on_delete=models.CASCADE,related_name='styles')
    service_price=models.PositiveIntegerField()
    custom_price=models.PositiveIntegerField()
    sale_format=models.CharField(max_length=50,default='FABRIC CUSTOM',choices=SALE_FORMATS)
    gender=models.CharField(max_length=50,default='F',choices=GENDER)
    pub_date=models.DateTimeField()
    fabrics=models.ManyToManyField(Fabrics,related_name="styles",blank=True)
    photo1=models.ImageField(upload_to=styles_file,blank=True,null=True)
    photo2=models.ImageField(upload_to=styles_file,blank=True,null=True)
    photo3=models.ImageField(upload_to=styles_file,blank=True,null=True)
    photo4=models.ImageField(upload_to=styles_file,blank=True,null=True)
    
    '''photo1=models.ImageField(upload_to=style_file)'''
    
    def publish(self):
        self.pub_date=timezone.now()
        self.save()
    
    def __str__(self):
        return self.name
        
class Accessories(models.Model):
    GENDER=(
        ('M', "Male"),
        ('F', 'Female'),
    )
    name=models.CharField(max_length=100)
    price=models.PositiveIntegerField()
    designer=models.ForeignKey(Designer,on_delete=models.CASCADE,related_name='accessories')
    gender=models.CharField(max_length=50,default='F',choices=GENDER)
    
    def __str__(self):
        return self.name
        


        
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,editable=True)
    city=models.CharField(max_length=15)
    country=models.ForeignKey(Country)
    address=models.TextField()
    
    
