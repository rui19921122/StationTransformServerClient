from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status

from article.models import Article
from .serializations import ArticleSer
import permissions as custom_permissions


# Create your views here.

class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        custom_permissions.AnyCanReadButOnlyOwnerCanUpdate,
    ]
    serializer_class = ArticleSer
    queryset = Article.objects.all()

    def get_object(self):
        """
        :rtype: Article
        :return:
        """
        obj = get_object_or_404(self.get_queryset().
                                filter(pk=self.kwargs.get('pk')))
        self.check_object_permissions(self.request, obj)
        return obj


class ArticleEditPermission(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        custom_permissions.OnlyOwnerCanOperate,
    ]
    serializer_class = ArticleSer
    queryset = Article.objects.all()

    def get_object(self):
        """
        :rtype: Article
        :return:
        """
        obj = get_object_or_404(self.get_queryset().
                                filter(pk=self.kwargs.get('pk')))
        self.check_object_permissions(self.request, obj)
        return obj
