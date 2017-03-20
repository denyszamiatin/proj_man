# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.
from ..models.user import User


def user_login(request):
    if request.method == 'POST':
        # was form add button clicked?
        if request.POST.get('login_button') is not None:
            errors = {}
            data = {}

            login = request.POST.get('email', '').strip()
            if not login:
                errors['login'] = u"Email is required"
            else:
                data['login'] = login

            pwd = request.POST.get('password', '').strip()
            if not pwd:
                errors['password'] = u"Password is required"
            else:
                data['password'] = pwd

            if not errors and User.objects.filter(email=data['email'])[0]:

                # redirect to students list
                return HttpResponseRedirect(
                    u'{}?status_message=Project successfully added!'.format(reverse('projects_list')))
            else:
                # render form with errors and previous user input
                text_member = ', '.join(members)
                return render(request, 'projects_add.html',
                              {'users': User.objects.all().order_by('login'),
                               'errors': errors,
                               'text_member': text_member
                               })
        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect(
                u'{}?status_message=Adding project is canceled!'.format(reverse('projects_list')))

    else:
        return render(request, 'projects_list.html', {'users': User.objects.all().order_by('login')})


