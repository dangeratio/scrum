from django.conf.urls import url
from django.views.generic import ListView
from projects.models import Project
from projects.views import ProjectDetail, ProjectCreate, ProjectUpdate, ProjectIndex


urlpatterns = [
    # Examples:
    # url(r'^$', 'scrum.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^$', ProjectIndex.as_view(template_name='project_index.html')),
    url(r'^view/(?P<pk>\d+)/$', ProjectDetail.as_view(template_name='project_view.html')),
    url(r'^create/$', ProjectCreate.as_view(template_name='project_edit.html')),
    url(r'^edit/(?P<pk>\d+)$', ProjectUpdate.as_view(template_name='project_edit.html')),
    url(r'^delete/(?P<pk>\d+)$', 'projects.views.delete'),

]
