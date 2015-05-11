from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
import projects.urls


urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^projects/', include(projects.urls)),
    url(r'^/$', RedirectView.as_view(url='/projects/', permanent=True)),
    url(r'^$', RedirectView.as_view(url='/projects/', permanent=True)),

    # ajax
    #
    url(r'^ajax/release_quick/(?P<release_id>\d+)/(?P<item_id>\d+)$', 'projects.views.release_quick_add_ajax'),
    url(r'^ajax/item_start/(?P<item_id>\d+)$', 'projects.views.item_start'),
    url(r'^ajax/item_complete_action/(?P<item_id>\d+)$', 'projects.views.item_complete_action'),
    url(r'^ajax/item_complete_no_action/(?P<item_id>\d+)$', 'projects.views.item_complete_no_action'),
    url(r'^ajax/item_add_comment/(?P<item_id>\d+)$', 'projects.views.item_add_comment'),
    url(r'^ajax/get_chart/(?P<project_id>\d+)/(?P<chart_id>\S+)$', 'projects.views.get_chart'),

]
