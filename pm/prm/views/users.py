# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.
from ..models.project import Project
from ..models.user import User
from ..models.member import Member


def validations(request) -> object:
    errors = {}
    data = {}

    # validate user input
    login = request.POST.get('login', '').strip()
    if not login:
        errors['login'] = u"Login is required"
    else:
        data['login'] = login

    email = request.POST.get('email', '').strip()
    if not email:
        errors['email'] = u'Email is required'
    else:
        data['email'] = email

    password = request.POST.get('password', '').strip()
    if not password:
        errors['password'] = u'Password is required'
    else:
        data['password'] = password

    c_password = request.POST.get('c_password', '').strip()
    if not c_password:
        errors['c_password'] = u'Password is required'
    else:
        if data['password'] and data['password'] != c_password:
            errors['c_password'] = u'Passwords did not match'

    return data, errors


def update_attrs(instance, **kwargs):

    instance_pk = instance.pk
    for key, value in kwargs.items():
        if hasattr(instance, key):
            setattr(instance, key, value)
        else:
            raise KeyError("Failed to update non existing attribute {}.{}".format(
                instance.__class__.__name__, key
            ))
    instance.save(force_update=True)
    return instance.__class__.objects.get(pk=instance_pk)


def users_list(request):
    users = User.objects.all()
    return render(request, 'users/users_list.html', {'users': users})


def users_add(request):
    if request.method == 'POST':
        # was form add button clicked?
        if request.POST.get('add_button') is not None:

            data, errors = validations(request)

            if data.get('login', '') and User.objects.filter(login=data['login']):
                errors['login'] = u"User with such login is already exist"

            if data.get('email', '') and User.objects.filter(email=data['email']):
                errors['email'] = u"User with such email is already exist"

            if not errors:
                user = User(**data)
                user.save()

                # redirect to students list
                return HttpResponseRedirect(u'{}?status_message=User successfully added!'.format(reverse('users_list')))
            else:
                # render form with errors and previous user input
                return render(request, 'users/users_add.html',
                              {'errors': errors,})
        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect(u'{}?status_message=Adding user is canceled!'.format(reverse('users_list')))

    else:
        return render(request, 'users/users_add.html', {})


def users_edit(request, pk):
    user = User.objects.filter(pk=pk)[0]
    if request.method == 'POST':
        # was form add button clicked?
        if request.POST.get('edit_button') is not None:

            data, errors = validations(request)

            if data.get('login', ''):
                v_user = User.objects.filter(login=data['login'])
                if v_user and v_user[0] != user:
                    errors['login'] = u"User with such login is already exist"

            if data.get('email', ''):
                v_user = User.objects.filter(email=data['email'])
                if v_user and v_user[0] != user:
                    errors['email'] = u"User with such email is already exist"

            if not errors:
                update_attrs(user, **data)

                # redirect to students list
                return HttpResponseRedirect(
                    u'{}?status_message=User is successfully saved!'.format(reverse('users_list')))
            else:
                # render form with errors and previous user input
                return render(request, 'users/users_edit.html',
                              {'users': User.objects.all().order_by('login'),
                               'errors': errors,
                               'user': user,
                               })
        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect(
                u'{}?status_message=Editing user is canceled!'.format(reverse('users_list')))

    else:
        return render(request, 'users/users_edit.html',
                      {'users': User.objects.all().order_by('login'), 'user': user})


def users_delete(request, pk):
    user = User.objects.filter(pk=pk)[0]

    if request.method == 'POST':

        # was form add button clicked?
        if request.POST.get('delete_button') is not None:
            user.delete()
            return HttpResponseRedirect(u'{}?status_message=User deleted!'.format(reverse('users_list')))

        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect(
                u'{}?status_message=Deletion of user is canceled!'.format(reverse('users_list')))

    else:
        return render(request, 'users/users_delete.html', {'user': user})

