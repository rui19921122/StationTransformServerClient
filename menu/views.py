from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from menu.models import Menu, MenuPickle
from django.http.response import Http404
from .serializations import MenuSer, AddChildSer, MenuAdministratorSer
from article.serializations import ArticleSer
import permissions as custom_permissions


# Create your views here.
class ListMenu(generics.ListCreateAPIView):
    """
    获取所有目录或添加根目录,不受理变更根目录请求
    """

    permission_classes = [custom_permissions.AnyCanReadButOnlySuperCanAdd]
    serializer_class = MenuSer

    def list(self, request, *args, **kwargs):
        """
        :type request: django.http.request.HttpRequest
        """
        menus = Menu.objects.all()
        return Response(data={
            'items': MenuSer(menus, many=True, context={'request': request}).data,
            'sort': MenuPickle.get_menu(),
        })

    def post(self, request, *args, **kwargs):
        """
        :type request: Request
        :return:
        """
        new = MenuSer(data=request.data,context={'request':request})
        if new.is_valid():
            new.save(owner_id=request.user.pk)
            return Response(data=new.data, status=status.HTTP_201_CREATED)
        else:
            raise ValidationError(new.errors)


class MenuDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    更改、删除目录具体内容
    """

    serializer_class = MenuSer
    queryset = Menu.objects.all()
    permission_classes = [custom_permissions.AnyCanReadButOnlyOwnerCanUpdate, ]

    def get_object(self):
        queryset = self.get_queryset()
        _filter = {'pk': int(self.kwargs.get('pk'))}
        obj = get_object_or_404(queryset, **_filter)
        self.check_object_permissions(self.request, obj)
        return obj


class MenuChildren(generics.ListCreateAPIView):
    """
    添加、查询目录子目录,只有目录的拥有者可以更改
    """
    serializer_class = MenuSer
    queryset = Menu.objects.all()
    permission_classes = [
        custom_permissions.AnyCanReadButOnlyOwnerCanUpdate
    ]

    def get_object(self):
        """
        :rtype :Menu
        """
        pk = int(self.kwargs.get('pk'))
        _filter = {'pk': pk}
        obj = get_object_or_404(self.get_queryset(),
                                **_filter
                                )
        self.check_object_permissions(self.request, obj)
        return obj

    def post(self, request, *args, **kwargs):
        """
        :type request:Request
        """
        ser = AddChildSer(data=request.data)
        ser.is_valid(raise_exception=True)
        name = ser.data.get('name')
        parent = self.get_object()
        new = Menu.objects.create(
            name=name,
            owner=request.user,
            parent=parent
        )
        return Response(data=MenuSer(new).data,
                        status=status.HTTP_201_CREATED
                        )


class MenuAdministratorList(generics.ListCreateAPIView):
    """
    添加、查询目录管理员，只有目录的拥有者才可以浏览和更改
    """
    queryset = Menu.objects.all()
    permission_classes = [
        custom_permissions.OnlyOwnerCanOperate,
    ]

    def get_object(self):
        """
        :rtype :Menu
        :return:
        """
        queryset = self.get_queryset()
        _filter = {'pk': int(self.kwargs.get('pk'))}
        obj = get_object_or_404(queryset,
                                **_filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        """
        :type request:Request
        """
        ser = MenuAdministratorSer(data=request.data)
        if ser.is_valid(raise_exception=True):
            obj = self.get_object()
            user = User.objects.get(pk=ser.validated_data.get('pk'))
            obj.administrators.add(user)
            return Response(status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """
        :type request:Request
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return Response(
            MenuAdministratorSer(self.get_object().administrators, many=True).data
        )


class MenuAdministratorDetail(generics.RetrieveDestroyAPIView):
    """
    更改指定菜单用户管理，只可查询或者删除
    """
    permission_classes = [custom_permissions.OnlyOwnerCanOperate, ]
    serializer_class = MenuAdministratorSer

    def get_object(self):
        """
        :rtype :User
        :return:
        """
        menu_pk = int(self.kwargs.get('menu_pk'))
        admin_pk = int(self.kwargs.get('admin_pk'))
        try:
            obj = Menu.objects.get(pk=menu_pk)
        except ObjectDoesNotExist:
            raise Http404
        self.check_object_permissions(self.request, obj)
        try:
            return obj.administrators.get(pk=admin_pk)
        except ObjectDoesNotExist:
            raise Http404


class MenuArticlesList(generics.ListCreateAPIView):
    permission_classes = [custom_permissions.AnyCanReadButOnlyOwnerOrAdministratorCanAddChild]
    serializer_class = ArticleSer

    def get_queryset(self):
        """
        :return:
        """
        try:
            obj = Menu.objects.get(pk=int(self.kwargs.get('pk')))
            self.check_object_permissions(self.request, obj)
        except ObjectDoesNotExist:
            raise Http404
        return obj.article_set

    def get_object(self):
        """
        :rtype:Menu
        :return:
        """
        try:
            obj = Menu.objects.get(pk=int(self.kwargs.get('pk')))
            self.check_object_permissions(self.request, obj)
            return obj
        except ObjectDoesNotExist:
            raise Http404

    def create(self, request, *args, **kwargs):
        obj = self.get_object()
        data = self.get_serializer_class()(data=request.data,
                                           context={'request': self.request}
                                           )
        if data.is_valid(raise_exception=True):
            data.save(
                create_person_id=request.user.pk,
                menu_id=obj.pk
            )
            return Response(data=data.data, status=status.HTTP_201_CREATED)
