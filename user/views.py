from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from django.http.request import HttpRequest
from rest_framework.permissions import IsAuthenticated


class UserInfo(RetrieveAPIView):
    """

    """
    permission_classes = [IsAuthenticated]

    def retrieve(self, request: HttpRequest, *args, **kwargs):
        user = request.user
        data = {'name': user.username,
                'admin_menu': [menu.pk for menu in user.managed_menus.all()],
                'owner_menu': [menu.pk for menu in user.owner_menus.all()],
                'is_admin': user.is_superuser
                }
        return Response(data=data)
