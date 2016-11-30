from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^info/$', views.UserInfo.as_view(),
        name='user-info'),
]
