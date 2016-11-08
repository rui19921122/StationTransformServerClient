from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from article.models import Article, File
from .serializations import ArticleSer, FileSer
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


class DeleteArticleFile(generics.DestroyAPIView):
    permission_classes = [
        custom_permissions.OnlyOwnerCanOperate
    ]
    queryset = File.objects.all()


@api_view(['POST','GET'])
def upload_file(request, pk):
    if request.method == 'GET':
        article = Article.objects.get(pk=pk)
        ser = FileSer(article.files,many=True)
        return Response(data=ser.data)
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)
        user = request.user
        article = Article.objects.get(pk=pk)
        if not article.create_person == user:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)
        article.files.add(
            File.objects.create(
                file=request.FILES['file'],
                name=request.FILES['file'].name,
                create_person=request.user
            )
        )
        return HttpResponse(status=status.HTTP_201_CREATED)