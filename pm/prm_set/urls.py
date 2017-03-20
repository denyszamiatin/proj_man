"""prm_set URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from prm.views.projects import projects_list, projects_add, projects_edit, projects_delete
from prm.views.users import users_list, users_add, users_edit, users_delete
from prm.views.login import user_login


urlpatterns = [

    #url(r'^$', user_login, name='login'),
    #url(r'^projects/$', projects_list, name='projects_list'),


    url(r'^$', users_list, name='users_list'),
    url(r'^users/add/$', users_add, name='users_add'),
    url(r'^users/(?P<pk>\d+)/edit/$', users_edit, name='users_edit'),
    url(r'^users/(?P<pk>\d+)/delete/$', users_delete, name='users_delete'),


    url(r'^projects/$', projects_list, name='projects_list'),
    url(r'^projects/add/$', projects_add, name='projects_add'),
    url(r'^projects/(?P<pk>\d+)/edit/$', projects_edit, name='projects_edit'),
    url(r'^projects/(?P<pk>\d+)/delete/$', projects_delete, name='projects_delete'),
    

    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'projects_list'}, name='auth_logout'),
    url(r'^register/complete/$', RedirectView.as_view(pattern_name='projects_list')),
    
    
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include('registration.backends.simple.urls', namespace='users'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
