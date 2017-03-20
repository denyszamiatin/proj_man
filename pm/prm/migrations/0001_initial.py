# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-17 11:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Members',
                'verbose_name': 'Member',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Name')),
                ('description', models.CharField(default='', max_length=256, null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name_plural': 'Projects',
                'verbose_name': 'Project',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=256, unique=True, verbose_name='Login')),
                ('email', models.EmailField(max_length=256, unique=True, verbose_name='Email')),
                ('password', models.CharField(max_length=256, verbose_name='Password')),
            ],
            options={
                'verbose_name_plural': 'Users',
                'verbose_name': 'User',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prm.User', verbose_name='Author'),
        ),
        migrations.AddField(
            model_name='member',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prm.Project', verbose_name='Project'),
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prm.User', verbose_name='User'),
        ),
    ]
