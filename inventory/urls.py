"""inventory URL Configuration

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
from django.conf.urls import url, include
from sales.models import Purchase, PurchaseItem
from stock.models import Item, Category, Manufacturer

from sales.views import print_receipt, test_receipt

from stock.views import ItemListAPIView, ItemDetailAPIView

from django.contrib import admin
from django_yaaac.manager import autocomplete

# import xadmin
# xadmin.autodiscover()
# from xadmin.plugins import xversion
# xversion.register_models()


urlpatterns = [
    # url(r'^', include('admin_steroids.urls')),
    url(r'^', include('grappelli.urls')),
    url(r'^', include(admin.site.urls)),
    
    #URLs for Printing
    url(r'^print/(?P<purchase_id>[0-9]+)/$', print_receipt, name='print'),
    url(r'^test_receipt/$', test_receipt, name='test_receipt'),

    #URLs for Notification
    
    #URLs for Rest API
    url(r'^item_api/$', ItemListAPIView.as_view(), name='item_api_lists'),
    url(r'^item_api/(?P<pk>\d+)/$', ItemDetailAPIView.as_view(), name='item_api_detail'),
]
admin.site.site_header = 'Inventory Management System'
admin.site.site_title = 'Inventory Management System'