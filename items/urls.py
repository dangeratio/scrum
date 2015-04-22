from django.conf.urls import url
from django.views.generic import ListView, DetailView
from items.models import Item
from items.views import ItemDetail, ItemCreate, ItemUpdate


urlpatterns = [
    # Examples:
    # url(r'^$', 'scrum.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^$', ListView.as_view(
        queryset=Item.objects.all(),     # .order_by("-created")
        template_name='item_index.html'
    )),
    url(r'^view/(?P<pk>\d+)/$', ItemDetail.as_view(template_name='item_view.html')),
    url(r'^create/$', ItemCreate.as_view(template_name='item_edit.html')),
    url(r'^edit/(?P<pk>\d+)$', ItemUpdate.as_view(template_name='item_edit.html')),
    url(r'^delete/(?P<pk>\d+)$', 'items.views.delete'),

]

