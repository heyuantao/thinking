"""WebSiteStatus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
from MainApplication.views import ServiceStatus, AddUrl,RemoveUrl,UrlList,\
     SiteStatus

urlpatterns = [
    url(r'^service/', ServiceStatus.as_view()),
    url(r'^url/add/', AddUrl.as_view()),
    url(r'^url/remove/', RemoveUrl.as_view()),
    url(r'^url/list/', UrlList.as_view()),
    url(r'^status/', SiteStatus.as_view()),
    url(r'^$', SiteStatus.as_view()),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
   
]

urlpatterns = format_suffix_patterns(urlpatterns)