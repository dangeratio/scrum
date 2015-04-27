from django.conf.urls import include, url
from django.contrib import admin
import projects.urls


urlpatterns = [
    # Examples:
    # url(r'^$', 'scrum.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^projects/', include(projects.urls)),

]
