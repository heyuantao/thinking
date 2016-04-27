from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from ipcamerastatus import settings
from MainApplication.views import  IndexPage
     
urlpatterns = [
    # Examples:
    # url(r'^$', 'ipcamerastatus.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', IndexPage.as_view()),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
    #url(r'^admin/', include(admin.site.urls)),
]

urlpatterns = format_suffix_patterns(urlpatterns)