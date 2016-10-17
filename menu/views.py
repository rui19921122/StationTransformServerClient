from django.shortcuts import render
from rest_framework import generics, response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from menu.models import Menu
from .serializations import MenuSer


# Create your views here.
class ListMenu(generics.ListCreateAPIView):
    """
    获取所有目录或添加目录
    """

    # queryset = Menu.objects.all()
    # serializer_class = MenuSer

    def list(self, request, *args, **kwargs):
        """
        :type request: django.http.request.HttpRequest
        """
        menus = Menu.objects.all().order_by('create_time')
        items = MenuSer(menus, many=True)
        return Response(data={
            'items': items,
            'sort': []
        })
