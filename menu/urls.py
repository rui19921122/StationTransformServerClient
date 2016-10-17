from django.conf.urls import url
from django.contrib import admin
from .views import ListMenu

urlpatterns = [
    url(r'^menu/$', ListMenu.as_view(), name='list-menu'),
]
