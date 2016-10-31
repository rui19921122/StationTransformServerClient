from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.ListMenu.as_view(),
        name='menu-list'),
    url(r'^articles/$', views.ListArticles.as_view(),
        name='menu-list'),
    url(r'^(?P<pk>\d{1,3})/$', views.MenuDetail.as_view(),
        name='menu-detail'),
    url(r'^(?P<pk>\d{1,3})/children/$',
        views.MenuChildren.as_view(),
        name='menu-child'),
    url(r'^(?P<pk>\d{1,3})/administrator/$',
        views.MenuAdministratorList.as_view(),
        name='menu-administrator'),
    url(r'^(?P<menu_pk>\d{1,3})/administrator/(?P<admin_pk>\d{1,3})/$',
        views.MenuAdministratorDetail.as_view(),
        name='menu-administrator-detail'),
    url(r'^(?P<pk>\d{1,3})/articles/$',
        views.MenuArticlesList.as_view(),
        name='menu-articles'),
]
