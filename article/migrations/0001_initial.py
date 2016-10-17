# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='文章名称', max_length=50)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField(verbose_name='内容')),
                ('create_person', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
            ],
            options={
                'verbose_name_plural': '文章列表',
                'verbose_name': '文章',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='附件名', max_length=50)),
                ('file', models.FileField(upload_to='', verbose_name='文件')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('create_person', models.ForeignKey(related_name='created_files', to=settings.AUTH_USER_MODEL, verbose_name='上传人')),
            ],
            options={
                'verbose_name_plural': '附件列表',
                'verbose_name': '附件',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='files',
            field=models.ManyToManyField(related_name='created_articles', to='article.File', verbose_name='附件'),
        ),
        migrations.AddField(
            model_name='article',
            name='menu',
            field=models.ForeignKey(to='menu.Menu', verbose_name='目录'),
        ),
    ]
