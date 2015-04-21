from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponseRedirect, HttpResponse

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'scrum.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # default redirect
    url(r'^$', lambda r: HttpResponseRedirect('/projects/')),

    # admin
    url(r'^admin/', include(admin.site.urls)),

    # user handling
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',
        name='logout'),

    # apps
    url(r'^projects/', include('projects.urls')),
    url(r'^releases/', include('releases.urls')),
    url(r'^items/', include('items.urls')),

]

