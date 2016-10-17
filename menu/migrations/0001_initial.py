# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='目录名称', max_length=50)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('enabled', models.BooleanField(verbose_name='启用标记', default=True)),
                ('administrators', models.ManyToManyField(blank=True, related_name='managed_menus', verbose_name='管理员', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(related_name='owner_menus', to=settings.AUTH_USER_MODEL, verbose_name='拥有人')),
                ('parent', models.ForeignKey(blank=True, to='menu.Menu', null=True, verbose_name='父项名称')),
            ],
            options={
                'verbose_name_plural': '目录列表',
                'verbose_name': '目录',
            },
        ),
    ]
