# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-17 03:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
        ('article', '0002_auto_20161017_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='menu',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='menu.Menu', verbose_name='目录'),
            preserve_default=False,
        ),
    ]
