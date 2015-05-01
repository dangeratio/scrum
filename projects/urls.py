from django.conf.urls import url, patterns
from projects.views import *


urlpatterns = patterns('',

    # projects
    #
    url(r'^$', ProjectIndex.as_view()),
    url(r'^(?P<pk>\d+)/$', ProjectDetail.as_view()),
    url(r'^create/$', ProjectCreate.as_view()),
    url(r'^quick/$', ProjectCreateQuick.as_view()),
    url(r'^edit/(?P<pk>\d+)/$', ProjectUpdate.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', ProjectDelete.as_view()),

    # releases
    #
    url(r'^(?P<project_id>\d+)/releases/$', ReleaseIndex.as_view()),
    url(r'^(?P<project_id>\d+)/releases/(?P<pk>\d+)$', ReleaseDetail.as_view()),
    url(r'^(?P<project_id>\d+)/releases/create/$', ReleaseCreate.as_view()),
    url(r'^(?P<project_id>\d+)/releases/edit/(?P<pk>\d+)$', ReleaseUpdate.as_view()),
    url(r'^(?P<project_id>\d+)/releases/quick/(?P<pk>\d+)$', ReleaseQuickAdd.as_view()),
    url(r'^(?P<project_id>\d+)/releases/delete/(?P<pk>\d+)$', ReleaseDelete.as_view()),

    # items
    #
    url(r'^(?P<project_id>\d+)/releases/(?P<release_id>\d+)/items/$', ItemIndex.as_view()),
    url(r'^(?P<project_id>\d+)/releases/(?P<release_id>\d+)/items/(?P<pk>\d+)/$', ItemDetail.as_view()),
    url(r'^(?P<project_id>\d+)/releases/(?P<release_id>\d+)/items/create/$', ItemCreate.as_view()),
    url(r'^(?P<project_id>\d+)/releases/(?P<release_id>\d+)/items/edit/(?P<pk>\d+)$', ItemUpdate.as_view()),
    url(r'^(?P<project_id>\d+)/releases/(?P<release_id>\d+)/items/delete/(?P<pk>\d+)$', ItemDelete.as_view()),

    # ajax
    #
    url(r'^ajax/release_quick/(?P<release_id>\d+)/(?P<item_id>\d+)$', 'projects.views.release_quick_add_ajax'),


)

'''



'''