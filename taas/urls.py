"""taas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from rest_framework import routers
from app import views
from django.conf import settings
from django.views import static

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'designers', views.DesignerViewSet)
router.register(r'custom-styles', views.CustomStylesViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^create-style/', views.CreateStyleViewSet.as_view()),
	url(r'^create-fabric/', views.CreateFabricViewSet.as_view()),
	url(r'^create-accessory/', views.CreateAccessoriesViewSet.as_view()),
    url(r'^new-code/',views.new_access_code),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    url(r'^media/(?P<path>.*)$',static.serve,{'document_root':settings.MEDIA_ROOT}),
    url(r'^custom-fabrics/(?P<pk>[0-9]+)/$', views.custom_fabrics_list),
    url(r'^filter-styles/$', views.query_styles_list),
    url(r'^update-user/$', views.update_user_info),
    url(r'^custom-accessories/(?P<pk>[0-9]+)/(?P<gender>\w+)/$', views.custom_accessories_list),
    url(r'^style-code/(?P<code>\w+)/$', views.get_style_by_style_code),
    url(r'^login/',views.login),
	url(r'^rate/(?P<pk>[0-9]+)/',views.rate),
    url(r'^designer-stats/',views.designer_stats),
    url(r'^confirm-order/',views.confirm_order),
    url(r'^get-user-orders/',views.get_user_orders),
    url(r'^get-designer-styles/(?P<pk>[0-9]+)/$',views.get_designer_styles),
	url(r'^get-designer-accessories-by-designer/$',views.get_designer_accessories_by_designer),
	url(r'^get-designer-fabrics-by-designer/$',views.get_designer_fabrics_by_designer),
    url(r'^get-designer-styles-by-designer/$',views.get_designer_styles_by_designer),
    url(r'^update-status/(?P<pk>[0-9]+)/(?P<status>\w+)/$', views.update_order_status),
	url(r'^get-designer-ratings-by-designer/$',views.get_designer_rating_by_designer),
	url(r'^get-designer-fabric-by-fabricCollection/([\w ]+)/$',views.get_designer_fabric_by_fabricCollection),
	url(r'^create-fabriccollection/$', views.CreateFabricCollectionsViewSet.as_view()),
	url(r'^get-designer-orders-by-designer/$',views.get_designer_orders_by_designer),
	url(r'^get-undelivered-designer-orders-by-designer/$',views.get_undelivered_designer_orders_by_designer),
    url(r'^get-designer-fabriccollection/$',views.get_designer_fabricCollection),
    url(r'^meas/$',views.measurement_list),
    url(r'^init-transaction/$', views.new_access_code),
    url(r'^get-user-names/',views.get_user_name),
    url(r'^get-designer-rating/(?P<pk>[0-9]+)/$',views.get_designer_rating),
    url(r'^is-designer-check/(?P<data>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.is_designer_check),
]

