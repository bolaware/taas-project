from django.contrib.auth.models import User
from .models import Designer,Country,Styles,Fabrics,Accessories
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email',)

class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:    
        model = Country
        fields=('name',)

class DesignerSerializer(serializers.HyperlinkedModelSerializer):
    country=CountrySerializer()
    user=UserSerializer()
    class Meta:
        model = Designer
        fields = ('pk','name','country','user','dp','city','address','average_rating')
        
        
class CustomStylesSerializer(serializers.HyperlinkedModelSerializer):
    designer=DesignerSerializer()
    class Meta:    
        model = Styles
        fields=('pk','name','gender','photo1','custom_price','designer')
        
class CustomFabricsSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Fabrics
        fields=('pk','name','photo1','price','designer')
        
        
class CustomAccessoriesSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Accessories
        fields=('pk','name','price','designer')