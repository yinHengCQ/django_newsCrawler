from django.conf.urls import url
import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'django_newsCrawler.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^$',views.getIndex),
    url('showData/$',views.getData),
    url('showJobData/$',views.getJob51Data)
]