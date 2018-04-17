# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.template.defaultfilters import slugify
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
import os,string,random
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_unicode


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
    filepath='{name}/dp/{name}.{ext}'.format(
        name=instance.name,ext=ext)
    return filepath  

def covers_file(instance,filename):
    name,ext=filename.split('.')
    filepath='{name}/cover_photo/{name}.{ext}'.format(
        name=instance.name,ext=ext)
    return filepath      

class Designer(models.Model):
    DELIVERY=(
        ('W', "Everywhere in the world"),
        ('C', 'Only in your base country'),
        ('CI', 'Only in your base city'),
    )
    delivery_statement=models.CharField(max_length=20,default="CI",choices=DELIVERY)
    name=models.CharField(max_length=100)
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,editable=True)
    dp=models.ImageField(upload_to=dp_file)
    cover_photo=models.ImageField(upload_to=covers_file)
    city=models.CharField(max_length=15)
    country=models.ForeignKey(Country)
    address=models.TextField()
    bio=models.TextField(default="We are a fashion company based in Lagos, we specialize in all African Attires and our customer's smile are a proof of our competency")
    
    
    @property
    def average_rating(self):
        avg=self.ratings_set.all().aggregate(models.Avg('rating'))['rating__avg']
        value=round(avg,1)
        return value
        
    @property
    def total_feeds(self):
        a=Authority.objects.get(id=self.id)
        return a.feed_set.all().count()
    
    
    def __str__(self):
        return self.name
        

 
class Transactions(models.Model):
    STATUS=(
        ('Successful', "Successful"),
        ('Unsuccessful', 'Unsuccessful'),
    )
    reference=models.CharField(max_length=50)
    amount=models.PositiveIntegerField()
    user=models.ForeignKey(User)
    status=models.CharField(max_length=50,default="Unsuccessful",choices=STATUS)
    
    def __str__(self):
        return self.reference
        

        
class Category(models.Model):
    name=models.CharField(max_length=50,blank=True,null=True)
    slug=models.SlugField(blank=True,null=True)
    description=models.TextField(blank=True,null=True)
    
    class Meta:
        ordering=["name"]

    def save(self,*args,**kwargs):
        self.slug=slugify(unicode(self.name))
        super(Category,self).save(*args,**kwargs)
    def __str__(self):
        return self.name
        
class FabricCollection(models.Model):
    name=models.CharField(max_length=50)
    designer=models.ForeignKey(Designer)
    
    class Meta:
        ordering=["name"]
	
	
    def thumbnail(self,user):
        try:
            fabrics=Fabrics.objects.filter(designer=user.designer,collection=self).order_by('-pub_date')
            fabric=fabrics[0]
            return fabric.photo1.url
        except:
            return smart_unicode('/media/dp/no_fabric_here.png')
        
    def __str__(self):
        return self.name
        
        
def fabrics_file(instance,filename):
    name,ext=filename.split('.')
    filepath='fabric_pic/{name}/{filename}'.format(
        name=instance.designer.name,filename=filename)
    return filepath          
        

class Fabrics(models.Model):
    name=models.CharField(max_length=100)
    brand=models.CharField(max_length=100,blank=True,null=True)
    price=models.PositiveIntegerField()
    designer=models.ForeignKey(Designer,on_delete=models.CASCADE,related_name='fabrics')
    photo1=models.ImageField(upload_to=fabrics_file,blank=True,null=True)
    photo2=models.ImageField(upload_to=fabrics_file,blank=True,null=True)
    pub_date=models.DateTimeField(default=timezone.now)
    collection=models.ForeignKey(FabricCollection,blank=True,null=True)
     
    def __str__(self):
        return self.name

@receiver(models.signals.post_delete, sender=Fabrics)
def auto_delete_dp_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    x=instance.photo1
    if x:
        if os.path.isfile(x.path):
            os.remove(x.path)
	x=instance.photo2
    if x:
        if os.path.isfile(x.path):
            os.remove(x.path)
    
def styles_file(instance,filename):
    name,ext=filename.split('.')
    filepath='{designer}/styles_pic/{name}/{filename}'.format(
        designer=instance.designer.name,name=instance.name,filename=filename)
    return filepath  
        
class Styles(models.Model):
    GENDER=(
        ('M', "Male"),
        ('F', 'Female'),
    )
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    code=models.CharField(max_length=6,default=id_generator(),unique=True)
    name=models.CharField(max_length=100)
    designer=models.ForeignKey(Designer,on_delete=models.CASCADE,related_name='styles')
    custom_price=models.PositiveIntegerField()
    gender=models.CharField(max_length=50,default='F',choices=GENDER)
    pub_date=models.DateTimeField(default=timezone.now)
    photo1=models.ImageField(upload_to=styles_file,blank=True,null=True)
    photo2=models.ImageField(upload_to=styles_file,blank=True,null=True)
    photo3=models.ImageField(upload_to=styles_file,blank=True,null=True)
    photo4=models.ImageField(upload_to=styles_file,blank=True,null=True)
    category=models.ForeignKey(Category,related_name='styles',blank=True,null=True)
    fabricCollection=models.ForeignKey(FabricCollection,blank=True,null=True)
    '''photo1=models.ImageField(upload_to=style_file)'''
    
    def publish(self):
        self.pub_date=timezone.now()
        self.save()
    
    def __str__(self):
        return self.name

@receiver(models.signals.pre_save, sender=Styles)
def auto_delete_dp_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Styles.objects.get(pk=instance.pk).photo1
    except Styles.DoesNotExist:
        return False

    new_file = instance.photo1
    if old_file:
        if not old_file==new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    try:
        old_file2 = Styles.objects.get(pk=instance.pk).photo2
    except Styles.DoesNotExist:
        return False

    new_file2 = instance.photo2
    if old_file2:
        if not old_file2==new_file2:
            if os.path.isfile(old_file2.path):
                os.remove(old_file2.path)
	
				
@receiver(models.signals.post_delete, sender=Styles)
def auto_delete_dp_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    x=instance.photo1
    if x:
        if os.path.isfile(x.path):
            os.remove(x.path)
	x=instance.photo2
    if x:
        if os.path.isfile(x.path):
            os.remove(x.path)
	x=instance.photo3
    if x:
        if os.path.isfile(x.path):
            os.remove(x.path)
	x=instance.photo4
    if x:
        if os.path.isfile(x.path):
            os.remove(x.path)
			
def accessories_file(instance,filename):
    name,ext=filename.split('.')
    filepath='{name}/accessories_pic/{filename}'.format(
        name=instance.designer.name,filename=filename)
    return filepath 
        
class Accessories(models.Model):
    GENDER=(
        ('M', "Male"),
        ('F', 'Female'),
    )
    name=models.CharField(max_length=100)
    price=models.PositiveIntegerField()
    designer=models.ForeignKey(Designer,on_delete=models.CASCADE,related_name='accessories')
    gender=models.CharField(max_length=50,default='F',choices=GENDER)
    pub_date=models.DateTimeField(default=timezone.now)
    photo1=models.ImageField(upload_to=accessories_file,blank=True,null=True)
    
    @property
    def abs_url(self):
        url=self.photo1.url
        return url
    
    def __str__(self):
        return self.name
        
@receiver(models.signals.post_delete, sender=Accessories)
def auto_delete_dp_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    x=instance.photo1
    if x:
        if os.path.isfile(x.path):
            os.remove(x.path)

        
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,editable=True)
    city=models.CharField(max_length=15)
    country=models.ForeignKey(Country)
    address=models.TextField()
    
class Order(models.Model):
    STATUS=(
        ('R', "Order received by Designer"),
        ('F', "Gotten the Fabric"),
        ('S', "Currently been sown"),
        ('D', "To be delivered today")
    )
    status=models.CharField(max_length=50,choices=STATUS,default='R')
    pub_date=models.DateTimeField(blank=True,null=True,auto_now_add=True)
    reference=models.CharField(max_length=50)
    transaction=models.OneToOneField(Transactions,on_delete=models.PROTECT,
        primary_key=True)
    style=models.ForeignKey(Styles)
    fabric=models.ForeignKey(Fabrics)
    accessories=models.ManyToManyField(Accessories)
    designer=models.ForeignKey(Designer)
    user=models.ForeignKey(User)
    amount=models.PositiveIntegerField()
    
    def publish(self):
        self.pub_date=timezone.now()
        self.save()
		
    @property
    def measurements(self):
        measurements = self.measurement_set.all()
        return measurements
        
    @property
    def is_rated(self):
        try:
            rating=self.ratings
            return True
        except ObjectDoesNotExist:
            return False
        return False
		
    def __str__(self):
        return self.reference    
        
class Ratings(models.Model):
    DEFAULT_ORDER_ID = 5
    rating=models.DecimalField(max_digits=2,decimal_places=1)
    responsiveness=models.DecimalField(max_digits=2,decimal_places=1,null=True)
    delivery_time=models.DecimalField(max_digits=2,decimal_places=1,null=True)
    quality=models.DecimalField(max_digits=2,decimal_places=1,null=True)
    comment=models.TextField()
    order=models.OneToOneField(Order)
    designer=models.ForeignKey(Designer)
	
    @property
    def user(self):
        user=self.order.user
        return user
	
    def __str__(self):
        return self.comment
        
class Measurement(models.Model):
    GENDER=(
        ('M', "Male"),
        ('F', 'Female'),
    )
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    gender= models.CharField(max_length=50,choices=GENDER)
    shoulder=models.DecimalField(max_digits=5,decimal_places=1,null=True,blank=True)
    chest=models.DecimalField(max_digits=5,decimal_places=1,null=True,blank=True)
    neck=models.DecimalField(max_digits=5,decimal_places=1,null=True,blank=True)
    tummy=models.DecimalField(max_digits=5,decimal_places=1,null=True,blank=True)
    top_half_length=models.DecimalField(max_digits=5,decimal_places=1,null=True,blank=True)
    top_length=models.DecimalField(max_digits=5,decimal_places=1,null=True,blank=True)
    long_sleeve=models.DecimalField(max_digits=5,decimal_places=1,null=True,blank=True)
    short_sleeve=models.DecimalField(max_digits=5,decimal_places=1,null=True,blank=True)
    round_sleeve=models.DecimalField(max_digits=5,decimal_places=1,null=True,blank=True)
    arm_hole=models.DecimalField(max_digits=5,decimal_places=1,null=True,blank=True)
    handcuff=models.DecimalField(max_digits=5,decimal_places=1,null=True,blank=True)
    waist=models.DecimalField(max_digits=5,decimal_places=1,null=True,blank=True)
    bum=models.DecimalField(max_digits=5,decimal_places=1,null=True,blank=True)
    lap=models.DecimalField(max_digits=5,decimal_places=1,null=True,blank=True)
    ankle=models.DecimalField(max_digits=5,decimal_places=1,null=True,blank=True)
    knee_length=models.DecimalField(max_digits=5,decimal_places=1,null=True,blank=True)
    trouser_length=models.DecimalField(max_digits=5,decimal_places=1,null=True,blank=True)
    flab=models.DecimalField(max_digits=5,decimal_places=1,null=True,blank=True)
    
    def __str__(self):             
        return self.name
    
