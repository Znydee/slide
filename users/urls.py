from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.home,name="slide-home" ),
    path('<slug:slug>',views.profile,name="profile" ),
]