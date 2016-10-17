from django.shortcuts import render
from rest_framework import generics, response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from menu.models import Menu


# Create your views here.
class GetMenu(generics.ListCreateAPIView):
    """
    获取所有目录或添加目录
    """
    queryset = Menu.objects.all()
    # serializer_class =

    def list(self, request, *args, **kwargs):
        """
        :type request: django.http.request.HttpRequest
        """
        pass
