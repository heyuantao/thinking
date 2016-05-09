from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'ipcamerastatus.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^ipcamera/', include('MainApplication.urls')),
    #url(r'^admin/', include(admin.site.urls)),
]
