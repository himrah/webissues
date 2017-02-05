"""webissues URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from track.views import *
from track import views
from django.contrib.auth.views import logout,login
from track.form import *
from rest_framework import routers
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf.urls import handler404

router=routers.DefaultRouter()
router.register('issue',IssueSet)
router.register('project',ProjectSet)
router.register('user',UserSet)


urlpatterns = [
    #url('',include('track.url',namespace='track')),
    url(r'^api/',include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',index,name='index'),
    url(r'^index/',index,name='index'),
    url(r'^accounts/login/',views.login,name='login'),
    url(r'^accounts/auth/',auth_view,name='auth'),
    url(r'^nav',TemplateView.as_view(template_name='new_nav.html')),
    url(r'^accounts/logout/',logout,{'template_name':'registration/logout.html'}),
    url(r'^accounts/profile/',profile,name='profile'),
    url(r'^accounts/auth/',auth_view,name='authview'),
    url(r'^total',noproject,name='number_of_project'),
    url(r'^issues/(?P<pk>\d+)/delete',delete_issue,name='delete_issue'),
    url(r'^issues/(?P<pk>\d+)/edit',edit,name='project_edit'),
    url(r'^issues/(?P<pk>\d+)$',issue_detail,name='issue_details'),
    url(r'^updateproject/(?P<pk>\d+)$',projectupdate,name='project_edit'),
    url(r'^project/(?P<pk>\d+)$',projectis_issue,name='project_issue'),
    url(r'^create/(?P<pk>\d+)$',create,name='create_issue'),
    url(r'^create/$',selectproject,name='project_selection'),
    url(r'^new/',new,name='new'),
    url(r'^edit/',edit,name='edit'),
    url(r'^delete/(?P<pk>\d+)$',delete_issues,name='delete'),
    url(r'^export',export_csv,name='csv'),
    url(r'^create/project$',create_project,name='create_project'),
    url(r'^search',searching,name='search'),
    url(r'^grade',grade,name='gradecard'),
    url(r'result',result,name='result'),
    url(r'^api/',include('rest_framework.urls',namespace='rest_framework'))
]