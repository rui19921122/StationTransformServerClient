from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
from menu.models import Menu


class Article(models.Model):
    name = models.CharField(verbose_name='文章名称', max_length=50)
    create_person = models.ForeignKey(User,
                                      verbose_name='创建人')
    create_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(verbose_name='内容',null=True,blank=True)
    files = models.ManyToManyField('article.File',
                                   related_name='created_articles',
                                   verbose_name='附件',
                                   )
    menu = models.ForeignKey('menu.Menu',
                             verbose_name='目录',
                             null=True,
                             on_delete=models.SET_NULL
                             )

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章列表'


class File(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='附件名')
    file = models.FileField(verbose_name='文件')
    create_time = models.DateTimeField(auto_now_add=True)
    create_person = models.ForeignKey(User,
                                      related_name='created_files',
                                      verbose_name='上传人')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '附件'
        verbose_name_plural = '附件列表'
