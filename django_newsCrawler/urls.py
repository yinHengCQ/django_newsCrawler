from django.conf.urls import include, url
from django.contrib import admin
from django_newsCrawler import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'django_newsCrawler.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('^',include('crawler.urls')),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
]
