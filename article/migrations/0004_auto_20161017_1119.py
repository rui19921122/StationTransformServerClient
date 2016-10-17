# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-17 03:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_article_menu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='files',
        ),
        migrations.AddField(
            model_name='article',
            name='files',
            field=models.ManyToManyField(related_name='created_articles', to='article.File', verbose_name='附件'),
        ),
    ]