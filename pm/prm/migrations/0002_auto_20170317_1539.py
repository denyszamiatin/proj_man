# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-17 13:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
    ]
