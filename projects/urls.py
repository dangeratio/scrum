from django.conf.urls import url
from django.views.generic import ListView
from projects.models import Project
from projects.views import ProjectDetail, ProjectCreate, ProjectUpdate, ProjectIndex



urlpatterns = [
    # Examples:
    # url(r'^$', 'scrum.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^$', ProjectIndex.as_view()),
    url(r'^view/(?P<pk>\d+)/$', ProjectDetail.as_view()),
    # url(r'^create/$', 'projects.views.create'),
    url(r'^create/$', ProjectCreate.as_view()),
    url(r'^edit/(?P<pk>\d+)$', ProjectUpdate.as_view()),
    url(r'^delete/(?P<pk>\d+)$', 'projects.views.delete'),

]
