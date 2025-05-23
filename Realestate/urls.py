"""Realestate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from realestateapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('login/',views.login),
    path('register_owner/',views.landowner_register),
    path('register_user/',views.user_register),
    path('adminHome/',views.adminHome),
    path('ownerHome/',views.ownerHome),
    path('userHome/',views.userHome),
    path('viewowners/',views.view_landowner),
    path('viewusers/',views.view_users),
    path('Approveowner/',views.approve_owners),
    path('addlandarea/',views.addlandarea),
    path('viewlandarea/',views.viewlandarea),
    path('viewdetails/',views.viewareadetail),
    path('viewland_user/',views.viewland),
    path('viewdetails_user/',views.viewdetail_user),
    path('bookland/',views.bookland),
    path('bookingdetail/',views.viewbooking),
    path('pay/',views.advancepayment),
    path('cancel/',views.cancelbooking),
    path('viewbooking_owner/',views.viewbookings_owner),
    path('approvebooking/',views.approvebooking),
    path('rejectbooking/',views.rejectbooking),
    path('editlanddetail/',views.editlanddetail),
    path('deleteland/',views.deleteland),
    path('viewbooking_admin/',views.viewBookings_admin),
    path('viewland_admin/',views.viewland_admin),
    path('viewdetails_admin/',views.viewdetail_admin),
    path('houseprice_predict/',views.house_price_predictor),

]
