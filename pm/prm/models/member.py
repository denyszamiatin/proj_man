from django.db import models

# Create your models here.


class Member(models.Model):
    class Meta(object):
        verbose_name = u'Member'
        verbose_name_plural = u'Members'

    project = models.ForeignKey('Project', verbose_name=u'Project', blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey('User', verbose_name=u'User', blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return u'{} is member of {}'.format(self.user, self.project)