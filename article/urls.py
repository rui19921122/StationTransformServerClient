from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^(?P<pk>\d{1,5})/$', views.ArticleDetail.as_view(),
        name='article-detail'),
]