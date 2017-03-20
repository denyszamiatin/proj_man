# -*- coding: utf-8 -*
from django.db import models


class User(models.Model):
    class Meta(object):
        verbose_name = u'User'
        verbose_name_plural = u'Users'

    login = models.CharField(max_length=256, blank=False, verbose_name=u"Login", unique=True)

    email = models.EmailField(max_length=256, blank=False, verbose_name=u'Email', unique=True)

    password = models.CharField(max_length=256, blank=False, verbose_name=u'Password')

    def __str__(self):
        return u'{}'.format(self.login)