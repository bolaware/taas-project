# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets
from .models import Designer,Country,Styles,Accessories
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import permissions
from .serializers import UserSerializer,DesignerSerializer,CountrySerializer,CustomStylesSerializer,CustomFabricsSerializer,CustomAccessoriesSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes=(permissions.IsAuthenticated,)
   
class DesignerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Designer.objects.all()
    serializer_class = DesignerSerializer
    
    
class CustomStylesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Styles.objects.filter(sale_format='BOTH').order_by('-pub_date')
    serializer_class = CustomStylesSerializer
    
    
@api_view(['GET', 'POST'])
def custom_styles_list(request,pk):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        style = Styles.objects.get(pk=pk)
        fabrics=style.fabrics.all()
        serializer = CustomFabricsSerializer(fabrics, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def custom_accessories_list(request,gender):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        accessories=Accessories.objects.filter(gender=gender)
        serializer = CustomAccessoriesSerializer(accessories, many=True)
        return Response(serializer.data) 
 
def login(request):
    if request.user.is_authenticated():
        print request.user.username
        return HttpResponse("logged in user")
    else:
        return HttpResponse("not logged in")
