"""
URL configuration for hhpnw project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from hhpnwapi.views import ItemView, OrderView, OrderItemView, RevenueView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'items', ItemView, 'item')
router.register(r'orders', OrderView, 'order')
router.register(r'orderitems', OrderItemView, 'orderitem')
router.register(r'revenues', RevenueView, 'revenue')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
