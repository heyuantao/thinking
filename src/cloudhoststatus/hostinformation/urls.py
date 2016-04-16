"""cloudhoststatus URL Configuration

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
from django.conf.urls import include,patterns
from rest_framework.urlpatterns import format_suffix_patterns
import hostinformation
from hostinformation.views import IndexPage,HostStatus,HostSetting

urlpatterns = [
    url(r'^$', IndexPage.as_view()),
    url(r'^settings/', HostSetting.as_view()),
    url(r'^status/', HostStatus.as_view()),
    #url(r'^admin/', admin.site.urls),
]

urlpatterns = format_suffix_patterns(urlpatterns)