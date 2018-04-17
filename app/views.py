# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from .models import Designer,Country,Styles,Accessories,Category,Profile,Fabrics,Order,Measurement,FabricCollection
from rest_framework.decorators import api_view,parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction
from rest_framework import permissions
from app.models import Transactions,Order
from django.utils import timezone
from django.db.models import Q
from rest_framework.views import APIView

from django.db.models import Q
from .serializers import MeasurementsSerializer,FabricCollectionSerializer,RatingSerializer,OrdersSerializer,UserSerializer,DesignerSerializer,CountrySerializer,CustomStylesSerializer,CustomFabricsSerializer,CustomAccessoriesSerializer

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
    queryset = Styles.objects.all().order_by('-pub_date')
    serializer_class = CustomStylesSerializer

class CreateStyleViewSet(APIView):
    queryset = Styles.objects.all()
    serializer_class = CustomStylesSerializer
    parser_classes = (MultiPartParser, FormParser,)
		
    def post(self, request,  format=None):
		fc=FabricCollection.objects.filter(designer=request.user.designer,name=request.data.get('fabricCollection'))
		fc=fc[0]
		category=Category.objects.get(name=request.data.get('category'))
		data=request.data
		print data
		Styles.objects.create(name=data.get('title'),pub_date=timezone.now(),gender=data.get('gender'),fabricCollection=fc,photo1=data.get('photo1'),photo2=data.get('photo2'),custom_price=data.get('custom_price'),designer=request.user.designer)
		return Response({'response':"Succesfully saved"})
		
class CreateFabricViewSet(APIView):
    queryset = Fabrics.objects.all()
    serializer_class = CustomFabricsSerializer
    parser_classes = (MultiPartParser, FormParser,)
		
    def post(self, request,  format=None):
		fc=FabricCollection.objects.filter(designer=request.user.designer,name=request.data.get('fabricCollection'))
		fc=fc[0]
		data=request.data
		print data
		Fabrics.objects.create(name=data.get('title'),brand=data.get('brand'),pub_date=timezone.now(),collection=fc,photo1=data.get('photo1'),price=data.get('custom_price'),designer=request.user.designer)
		return Response({'response':"Succesfully saved"})
		
class CreateAccessoriesViewSet(APIView):
    queryset = Accessories.objects.all()
    serializer_class = CustomAccessoriesSerializer
    parser_classes = (MultiPartParser, FormParser,)
		
    def post(self, request,  format=None):
		data=request.data
		print data
		Accessories.objects.create(name=data.get('title'),gender=data.get('gender'),pub_date=timezone.now(),photo1=data.get('photo1'),price=data.get('price'),designer=request.user.designer)
		return Response({'response':"Succesfully saved"})		
	
@api_view(['POST'])
@parser_classes((JSONParser,))
def update_user_info(request):
    c=Country.objects.get(name=request.data['country'])
    u=User.objects.get(username=request.data['username'])
    u.first_name=request.data['first_name']
    u.last_name=request.data['last_name']
    u.save()
    Profile.objects.create(user=u,country=c,address=request.data['address'],city=request.data['city'])
    return Response({'first_name':request.data['first_name'],'last_name':request.data['last_name'],'address':request.data['address'],'country':request.data['country'],'city':request.data['city']})

@api_view(['GET'])
@parser_classes((JSONParser,))
def get_designer_rating(request,pk):
    d=get_object_or_404(Designer,pk=pk)
    ratings=d.ratings_set.all()
    serializer=RatingSerializer(ratings,context={'request': request}, many=True)
    return Response(serializer.data)
	
@api_view(['GET'])
@parser_classes((JSONParser,))
def get_designer_rating_by_designer(request):
    d=request.user.designer
    ratings=d.ratings_set.all()
    serializer=RatingSerializer(ratings,context={'request': request}, many=True)
    return Response(serializer.data)
	
@api_view(['GET'])
@parser_classes((JSONParser,))
def get_designer_orders_by_designer(request):
    d=request.user.designer
    orders=Order.objects.filter(designer=d)
    serializer=OrdersSerializer(orders,context={'request': request}, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@parser_classes((JSONParser,))
def get_undelivered_designer_orders_by_designer(request):
    d=request.user.designer
    orders=Order.objects.filter(designer=d).filter(Q(status="R") | Q(status="F") | Q(status="S"))
    serializer=OrdersSerializer(orders,context={'request': request}, many=True)
    return Response(serializer.data)
    
@api_view(['GET'])
@parser_classes((JSONParser,))
def designer_stats(request):
    u=request.user
    if not u.is_authenticated():
        return Response({'detail':"Unauthorized request"})
    try:
        designer=u.designer
        designer_serializer = DesignerSerializer(designer,context={'request': request})
        average_rating=designer.average_rating
        styles_num=designer.styles.all().count()
        fabrics_num=designer.fabrics.all().count()
        accessories_num=designer.accessories.all().count()
        orders=Order.objects.filter(designer=designer)
        order_num=orders.count()
        delivered_orders=orders.filter(status="D").count()
        undelivered_orders=order_num - delivered_orders
        fabricCollectionNumber=FabricCollection.objects.filter(designer=designer).count()
        return Response({'rating':average_rating,'designer':designer_serializer.data,'accessoriesNum':accessories_num,'stylesNum':styles_num,'fabricsNum':fabrics_num,'fabricCollectionNumber':fabricCollectionNumber,'unDeliveredOrdersNum':undelivered_orders,'ordersNum':order_num})

    except:
        return Response({'request':"Unauthorized request"})
    return Response({'request':"Unauthorized request"})
   
@api_view(['GET'])
@parser_classes((JSONParser,))
def get_style_by_style_code(request,code):
    style=get_object_or_404(Styles,code=code.upper())
    serializer=CustomStylesSerializer(style,context={'request': request},)
    return Response(serializer.data)

@api_view(['POST'])
@parser_classes((JSONParser,))
def rate(request,pk):
    o=get_object_or_404(Order,pk=pk)
    responsiveness=request.data['responsiveness']
    quality=request.data['quality']
    delivery_time=request.data['delivery_time']
    rating=responsiveness+quality+delivery_time
    rating=rating/3
    rating=round(rating,1)
    Ratings.objects.create(order=o,rating=rating,responsiveness=request.data['responsiveness'],quality=request.data['quality'],delivery_time=request.data['delivery_time'],comment=request.data['comment'],designer=o.designer)
    return Response({'response':"Succesfully saved"})	
	
@api_view(['GET'])
@parser_classes((JSONParser,))
def is_designer_check(request,data):
    try:
        u=User.objects.get(username=data)
    except:
        u=User.objects.get(email=data)
    if request.user != u:
        return Response({'detail':"Unauthorized request"}) 
    try:
        designer=u.designer
        serializer=DesignerSerializer(designer,context={'request': request})
        return Response(serializer.data) 
    except:
        return Response({'detail':"Unauthorized request,you not a designer"})   
    return Response({'detail':"Unauthorized request"})        
        
    ratings=d.ratings_set.all()
    serializer=RatingSerializer(ratings,context={'request': request}, many=True)
    return Response(serializer.data)    
    

@api_view(['POST'])
@parser_classes((JSONParser,))
def get_user_name(request):
    try:
        u=User.objects.get(username=request.data['username'])
    except:
        u=User.objects.get(email=request.data['username'])
    first_name=u.first_name
    last_name=u.last_name
    profile=u.profile
    country=profile.country.name
    city=profile.city
    return Response({'first_name':first_name,'last_name':last_name,"country":country,"city":city})

@api_view(['POST'])
@parser_classes((JSONParser,))
def get_user_orders(request):
    try:
        u=User.objects.get(username=request.data['username'])
    except:
        u=User.objects.get(email=request.data['username'])
    if request.user.is_authenticated() and request.user == u:
        orders=u.order_set.all()
        serializer=OrdersSerializer(orders,context={'request': request}, many=True)
        return Response(serializer.data)
    else:
        return Response({'detail':"Unauthorized request"})    
        
@api_view(['GET'])
@parser_classes((JSONParser,))
def get_designer_styles(request,pk):
    d=get_object_or_404(Designer,pk=pk)
    styles=d.styles.all()
    serializer=CustomStylesSerializer(styles,context={'request': request}, many=True)
    return Response(serializer.data)
    
@api_view(['GET'])
@parser_classes((JSONParser,))
def get_designer_accessories_by_designer(request):
    d=request.user.designer
    accessories=d.accessories.all()
    serializer=CustomAccessoriesSerializer(accessories,context={'request': request}, many=True)
    return Response(serializer.data)
	
@api_view(['GET'])
@parser_classes((JSONParser,))
def get_designer_fabrics_by_designer(request):
    d=request.user.designer
    fabrics=d.fabrics.all()
    serializer=CustomFabricsSerializer(fabrics,context={'request': request}, many=True)
    return Response(serializer.data)
	

@api_view(['GET'])
@parser_classes((JSONParser,))
def get_designer_styles_by_designer(request):
    u=request.user
    if not u.is_authenticated():
        return Response({'detail':"Unauthorized request"})
    try:
        d=u.designer
    except:
        return Response({'detail':"Unauthorized request"}) 
    styles=d.styles.all()
    serializer=CustomStylesSerializer(styles,context={'request': request}, many=True)
    return Response(serializer.data)    
    
    
@api_view(['GET'])
@parser_classes((JSONParser,))
def get_designer_fabric_by_fabricCollection(request,name):
    u=request.user
    if not u.is_authenticated():
        return Response({'detail':"Unauthorized request"})
    fc=FabricCollection.objects.get(name=name,designer=u.designer)
    fabrics = Fabrics.objects.filter(designer=u.designer,collection=fc)
    serializer=CustomFabricsSerializer(fabrics,context={'request': request}, many=True)
    return Response(serializer.data) 

@api_view(['GET'])
@parser_classes((JSONParser,))
def update_order_status(request,pk,status):
    try:
        if o.designer != request.user.designer:
            return Response({'response':"Unauthorized request"})
    except:
        o=get_object_or_404(Order,pk=pk)
        o.status=status
        o.save()
        return Response({'response':"Succesfully saved"})
    return Response({'response':"An error occured"})
    	
class CreateFabricCollectionsViewSet(APIView):
    queryset = FabricCollection.objects.all()
    serializer_class = FabricCollectionSerializer
    parser_classes = (MultiPartParser, FormParser,)
		
    def post(self, request,  format=None):
		data=request.data
		print data
		FabricCollection.objects.create(name=data.get('name'),designer=request.user.designer)
		return Response({'response':"Succesfully saved"})	
    
@api_view(['GET'])
@parser_classes((JSONParser,))
def get_designer_fabricCollection(request):
    u=request.user
    if not u.is_authenticated():
        return Response({'detail':"Unauthorized request"})
    try:
        d=u.designer
    except:
        return Response({'detail':"Unauthorized request"}) 
    fc=FabricCollection.objects.filter(designer=d)
    serializer=FabricCollectionSerializer(fc,context={'request': request}, many=True)
    return Response(serializer.data)
    
@api_view(['POST'])
@parser_classes((JSONParser,))
def new_access_code(request):
    paystack_secret_key = "##########"
    paystack = Paystack(secret_key=paystack_secret_key)
    response=Transaction.initialize(reference=request.data['reference'],amount=request.data['amount'],email=request.data['email'])
    Transactions.objects.create(user=User.objects.get(email=request.data['email']),reference=request.data['reference'],amount=request.data['amount'])
    print response
    return Response({'InitialTransactions':response}) 

@api_view(['POST'])
@parser_classes((JSONParser,))
def confirm_order(request):

    t=Transactions.objects.get(reference=request.data['reference'])
    t.status="Successful"
    t.save()
    s=Styles.objects.get(pk=request.data['style_pk'])
    print request.data
    f=Fabrics.objects.get(pk=request.data['fabric_pk'])
    a=[]
    
    
    for value in request.data['accessories']:
        accessory=Accessories.objects.get(pk=value)
        a.append(accessory)
    o=Order.objects.create(transaction=t,amount=t.amount,fabric=f,user=t.user,designer=s.designer,style=s,reference=t.reference,accessories=a)    
    for value in request.data['measurement']:
        print value
        Measurement.objects.create(order=o,name=value['name'],gender=value['gender'],shoulder=value['shoulder'],chest=value['chest'],neck=value['neck'],tummy=value['tummy'],top_half_length=value['top_half_length'],top_length=value['top_length'],long_sleeve=value['long_sleeve'],short_sleeve=value['short_sleeve'],round_sleeve=value['round_sleeve'],arm_hole=value['arm_hole'],handcuff=value['handcuff'],waist=value['waist'],bum=value['bum'],lap=value['lap'],ankle=value['ankle'],knee_length=value['knee_length'],trouser_length=value['trouser_length'],flab=value['flab'])
    
    return Response({'received order':"successful"})
    
@api_view(['GET'])
def query_styles_list(request):
    if request.method == 'GET':
        i=0
        list=[request.GET['c1'],request.GET['c2']]
        for x in list:
            if x == "":
                x = "rubbish"
            else:
                i+=1
        if i>0:
            """
            If at least one category is picked
            """
            c=Category.objects.filter(Q(name=request.GET['c1'])|Q(name=request.GET['c2']))
            s=Styles.objects.filter(designer__name__icontains=request.GET['designer'],
            custom_price__range=(request.GET['min'],request.GET['max']),
            gender__icontains=request.GET['gender'],
            category__in=c
            )
        
        else:
            """
            If no category is picked
            """
            s=Styles.objects.filter(designer__name__icontains=request.GET['designer'],
            custom_price__range=(request.GET['min'],request.GET['max']),
            gender__icontains=request.GET['gender'])
        
        serializer= CustomStylesSerializer(s,context={'request': request},many=True)
        return Response(serializer.data)
            
    
    
@api_view(['GET', 'POST'])
def custom_fabrics_list(request,pk):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        style = Styles.objects.get(pk=pk)
        fabricCollection = style.fabricCollection
        fabrics=Fabrics.objects.filter(collection=fabricCollection,designer=style.designer)
        serializer = CustomFabricsSerializer(fabrics,context={'request': request}, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def custom_accessories_list(request,pk,gender):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        designer=Designer.objects.get(pk=pk)
        accessories=Accessories.objects.filter(designer=designer,gender=gender)
        serializer = CustomAccessoriesSerializer(accessories,context={'request': request}, many=True)
        return Response(serializer.data) 
        
        
@api_view(['GET', 'POST'])
def measurement_list(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        measurement_list=Measurement.objects.all()
        serializer = MeasurementsSerializer(measurement_list,context={'request': request}, many=True)
        return Response(serializer.data) 
        
def login(request):
    if request.user.is_authenticated():
        print request.user.username
        return HttpResponse("logged in user")
    else:
        return HttpResponse("not logged in")
        

