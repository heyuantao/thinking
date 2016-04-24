"""networkhoststatus URL Configuration

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
from MainApplication.views import ServiceStatus, AddNetwork,RemoveNetwork,NetworkList,\
     NetworkStatus, IndexPage
     
urlpatterns = [
    url(r'^$', IndexPage.as_view()),
    url(r'^service/', ServiceStatus.as_view()),
    url(r'^network/add/', AddNetwork.as_view()),
    url(r'^network/remove/', RemoveNetwork.as_view()),
    url(r'^network/list/', NetworkList.as_view()),
    url(r'^status/', NetworkStatus.as_view()),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
]

urlpatterns = format_suffix_patterns(urlpatterns)
