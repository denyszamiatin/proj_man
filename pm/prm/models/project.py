# -*- coding: utf-8 -*
from django.db import models


class Project(models.Model):
    class Meta(object):
        verbose_name = u'Project'
        verbose_name_plural = u'Projects'

    name = models.CharField(max_length=256, blank=False, verbose_name=u"Name", unique=True)

    author = models.ForeignKey('User', verbose_name=u'Author', blank=False, null=True, on_delete=models.SET_NULL)

    description = models.TextField(blank=True, verbose_name=u'Description')

    def __str__(self):
        return u'{}'.format(self.name)
