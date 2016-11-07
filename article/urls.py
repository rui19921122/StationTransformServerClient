from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^(?P<pk>\d{1,5})/$', views.ArticleDetail.as_view(),
        name='article-detail'),
    url(r'^(?P<pk>\d{1,5})/files/$', views.upload_file,
        name='article-detail'),
    url(r'^(?P<pk>\d{1,5})/edit/$', views.ArticleEditPermission.as_view(),
        name='article-edit'),
    url(r'^file/(?P<pk>\d{1,5})/$', views.DeleteArticleFile.as_view(),
        name='delete-file'),
]
