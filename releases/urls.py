from django.conf.urls import url
from django.views.generic import ListView

from releases.models import Release
from releases.views import ReleaseDetail, ReleaseIndex, ReleaseUpdate


urlpatterns = [
    # Examples:
    # url(r'^$', 'scrum.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^$', ListView.as_view(
        queryset=Release.objects.all(),     # .order_by("-created")
        template_name='release_index.html'
    )),
    url(r'^view/(?P<pk>\d+)/$', ReleaseDetail.as_view(template_name='release_view.html')),
    url(r'^create/$', ReleaseIndex.as_view(template_name='release_edit.html')),
    url(r'^edit/(?P<pk>\d+)$', ReleaseUpdate.as_view(template_name='release_edit.html')),
    url(r'^delete/(?P<pk>\d+)$', 'releases.views.delete'),

]
