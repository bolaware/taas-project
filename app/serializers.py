from django.contrib.auth.models import User
from .models import Designer,Country,Measurement,Styles,Fabrics,Accessories,Order,Ratings,FabricCollection,Category
from rest_framework import serializers

from djoser import constants



        
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'first_name','last_name','username',)

class MeasurementsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Measurement
        fields=('name','gender','shoulder','chest','neck','tummy','top_half_length','top_length','long_sleeve','short_sleeve','round_sleeve','arm_hole','handcuff','waist','bum','lap','ankle','knee_length','trouser_length','flab')

class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:    
        model = Country
        fields=('name',)
        
class RatingSerializer(serializers.HyperlinkedModelSerializer):
    user=UserSerializer
    class Meta:    
        model = Ratings
        fields=('pk','comment','rating','quality','responsiveness','user','delivery_time')        

class DesignerSerializer(serializers.HyperlinkedModelSerializer):
    country=CountrySerializer()
    user=UserSerializer()
    class Meta:
        model = Designer
        fields = ('pk','name','country','bio','cover_photo','delivery_statement','user','dp','city','address','average_rating')
        
class FabricCollectionSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    numberOfFabrics = serializers.SerializerMethodField()
	
    class Meta:    
        model = FabricCollection
        fields=('name','thumbnail','numberOfFabrics')
    def get_thumbnail(self,fabricCollection):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        thumbnail=fabricCollection.thumbnail(user)
        return request.build_absolute_uri(thumbnail)
		
    def get_numberOfFabrics(self,fabricCollection):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        try:
            number = Fabrics.objects.filter(designer=user.designer,collection=fabricCollection).count()
        except:
		    number=0
        return number
		

class CategorySerializer(serializers.ModelSerializer):
    class Meta:    
        model = Category
        fields=('name',)  
        
class CustomStylesSerializer(serializers.HyperlinkedModelSerializer):
    designer=DesignerSerializer()
    fabricCollection=FabricCollectionSerializer()
    category=CategorySerializer()
    class Meta:    
        model = Styles
        fields=('pk','name','gender','fabricCollection','category','photo1','photo2','custom_price','designer')
        
class CustomFabricsSerializer(serializers.ModelSerializer):
    designer=DesignerSerializer()
    class Meta:    
        model = Fabrics
        fields=('pk','name','photo1','price','designer')
        
        
class CustomAccessoriesSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Accessories
        fields=('pk','name','price','photo1','designer')
 
class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields=('name','gender','shoulder','chest','neck','tummy','top_half_length','top_length','long_sleeve','short_sleeve','round_sleeve','arm_hole','handcuff','waist','bum','lap','ankle','knee_length','trouser_length','flab')

        
class OrdersSerializer(serializers.HyperlinkedModelSerializer):
    style=CustomStylesSerializer()
    fabric=CustomFabricsSerializer()
    accessories=CustomAccessoriesSerializer(many=True,read_only=True)
    pub_date=serializers.DateTimeField(format='%a %d %b,%y %I:%M%p')
    measurements=MeasurementSerializer(many=True,read_only=True)
    class Meta:
        model = Order
        fields = ('pk','reference', 'amount', 'style','is_rated','fabric','status','pub_date','accessories','measurements')
    