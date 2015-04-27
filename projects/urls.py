from django.conf.urls import url, patterns
from projects.views import *


urlpatterns = patterns('',

    # projects
    #
    url(r'^$', ProjectIndex.as_view()),
    url(r'^(?P<pk>\d+)/$', ProjectDetail.as_view(slug_field='project_id')),
    url(r'^create/$', ProjectCreate.as_view()),
    url(r'^edit/(?P<pk>\d+)/$', ProjectUpdate.as_view(slug_field='project_id')),
    url(r'^delete/(?P<pk>\d+)/$', 'projects.views.project_delete'),

    # releases
    #
    url(r'^(?P<project_id>\d+)/releases/$', ReleaseIndex.as_view()),
    url(r'^(?P<project_id>\d+)/releases/(?P<pk>\d+)$', ReleaseDetail.as_view(template_name='release_view.html')),
    url(r'^(?P<project_id>\d+)/releases/create/$', ReleaseCreate.as_view(template_name='release_edit.html')),
    url(r'^(?P<project_id>\d+)/releases/edit/(?P<pk>\d+)$', ReleaseUpdate.as_view(template_name='release_edit.html')),
    url(r'^(?P<project_id>\d+)/releases/delete/(?P<pk>\d+)$', 'projects.views.release_delete'),

    # items
    #
    url(r'^(?P<project_id>\d+)/releases/(?P<release_id>\d+)/items/$', ItemIndex.as_view()),
    url(r'^(?P<project_id>\d+)/releases/(?P<release_id>\d+)/items/(?P<pk>\d+)/$', ItemDetail.as_view()),
    url(r'^(?P<project_id>\d+)/releases/(?P<release_id>\d+)/items/create/$', ItemCreate.as_view()),
    url(r'^(?P<project_id>\d+)/releases/(?P<release_id>\d+)/items/edit/(?P<pk>\d+)$', ItemUpdate.as_view()),
    url(r'^(?P<project_id>\d+)/releases/(?P<release_id>\d+)/items/delete/(?P<pk>\d+)$', 'projects.views.item_delete'),


)

'''



'''