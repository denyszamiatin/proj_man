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
    data = {'description': request.POST.get('notes').strip()}

    members = [member[7:] for member in request.POST if 'member' in member]

    # validate user input
    name = request.POST.get('name', '').strip()
    if not name:
        errors['name'] = u"Name is required"
    else:
        data['name'] = name

    author = request.POST.get('author', '').strip()
    if not author:
        errors['author'] = u'Select author for your project'
    else:
        user = User.objects.filter(pk=author)
        if len(user) != 1:
            errors['student_group'] = u'Select correct user'
        else:
            data['author'] = user[0]

    return data, members, errors


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


def projects_list(request):
    projects = Project.objects.all()
    members = Member.objects.all()
    return render(request, 'projects/projects_list.html', {'projects': projects, 'members': members})


def projects_add(request):
    if request.method == 'POST':
        # was form add button clicked?
        if request.POST.get('add_button') is not None:

            data, members, errors = validations(request)

            if data.get('name', '') and Project.objects.filter(name=data['name']):
                errors['name'] = u"Project with such name is already exist"

            if not errors:
                project = Project(**data)
                project.save()
                if members:
                    prj = Project.objects.filter(name=data['name'])[0]
                    for memb in members:
                        user = User.objects.filter(login=memb)[0]
                        member = Member(project=prj, user=user)
                        member.save()
                # redirect to students list
                return HttpResponseRedirect(u'{}?status_message=Project successfully added!'.format(reverse('projects_list')))
            else:
                # render form with errors and previous user input
                text_member = ', '.join(members)
                return render(request, 'projects/projects_add.html',
                              {'users': User.objects.all().order_by('login'),
                               'errors': errors,
                               'text_member': text_member
                               })
        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect(u'{}?status_message=Adding project is canceled!'.format(reverse('projects_list')))

    else:
        return render(request, 'projects/projects_add.html', {'users': User.objects.all().order_by('login')})


def projects_edit(request, pk):
    project = Project.objects.filter(pk=pk)[0]
    db_members = [member.user for member in Member.objects.filter(project=project)]
    if request.method == 'POST':
        # was form add button clicked?
        if request.POST.get('edit_button') is not None:

            data, members, errors = validations(request)

            if data.get('name', ''):
                v_project = Project.objects.filter(name=data['name'])
                if v_project and v_project[0] != project:
                    errors['name'] = u"Project with such name is already exist"

            if not errors:
                update_attrs(project, **data)
                if members:
                    prj = Project.objects.filter(name=data['name'])[0]

                    for db_m in db_members:
                        if db_m.login not in members:
                            member = Member.objects.filter(project=project, user=db_m)[0]
                            member.delete()

                    for memb in members:
                        user = User.objects.filter(login=memb)[0]
                        if user not in db_members:
                            member = Member(project=prj, user=user)
                            member.save()


                # redirect to students list
                return HttpResponseRedirect(u'{}?status_message=Project is successfully saved!'.format(reverse('projects_list')))
            else:
                # render form with errors and previous user input
                text_member = ', '.join(members)
                return render(request, 'projects/projects_edit.html',
                              {'users': User.objects.all().order_by('login'),
                               'errors': errors,
                               'project': project,
                               'text_member': text_member
                               })
        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect(u'{}?status_message=Editing project is canceled!'.format(reverse('projects_list')))

    else:
        return render(request, 'projects/projects_edit.html',
                      {'users': User.objects.all().order_by('login'), 'members': db_members, 'project': project})


def projects_delete(request, pk):
    project = Project.objects.filter(pk=pk)[0]

    if request.method == 'POST':

        # was form add button clicked?
        if request.POST.get('delete_button') is not None:
            project.delete()
            return HttpResponseRedirect(u'{}?status_message=Project deleted!'.format(reverse('projects_list')))

        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect(u'{}?status_message=Deletion of project is canceled!'.format(reverse('projects_list')))

    else:
        return render(request, 'projects/projects_delete.html', {'project': project})

