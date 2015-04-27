from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django import http
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import context


from projects.models import Project, Release, Item
from projects import forms


# usage: raise DebugMessage('asdf')
class DebugMessage(Exception):

    def __init__(self, msg="Something went wrong."):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


#
#   Projects
#


class ProjectIndex(ListView):
    model = Project
    template_name = 'project_index.html'


class ProjectDetail(DetailView):
    model = Project
    template_name = 'project_view.html'
    slug_field = 'project_id'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        project_id = self.kwargs['pk']
        releases = Release.objects.filter(project=project_id)
        context['releases'] = releases
        return context


class ProjectCreate(CreateView):
    model = Project
    template_name = 'project_edit.html'
    form_class = forms.ProjectForm
    success_url = '/projects/'

    def post(self, request, *args, **kwargs):
        # create the project object and save it


        # create a "backlog" release to start out with


        # get project id for success url to redirect to the view of the project you just created
        project_id = ''
        self.success_url = '/projects/project_id'.replace("project_id", project_id)
        return super(ProjectCreate, self).post(request, *args, **kwargs)


class ProjectUpdate(UpdateView):
    model = Project
    template_name = 'project_edit.html'
    form_class = forms.ProjectForm
    success_url = '/projects/'
    slug_field = 'project_id'


def project_delete(request, pk):
    Project.objects.filter(pk=pk).delete()
    slug_field = 'project_id'
    return http.HttpResponseRedirect('/projects/')


#
#   Releases
#


class ReleaseIndex(ListView):
    model = Release
    template_name = 'release_index.html'

    def get_queryset(self):
        object_list = Release.objects.all()     # (project__id=self.kwargs['project_id'])
        return object_list


class ReleaseDetail(DetailView):

    model = Release

    def get_context_data(self, **kwargs):
        context = super(ReleaseDetail, self).get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        release_id = self.kwargs.get('pk')
        context['project_id'] = project_id
        items = Item.objects.filter(release=release_id)
        context['items'] = items
        return context


class ReleaseCreate(CreateView):

    model = Release
    # template_name = 'edit.html'
    form_class = forms.ReleaseForm
    success_url = '/releases/'

    def get_context_data(self, **kwargs):
        context = super(ReleaseCreate, self).get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        context['project_id'] = project_id
        self.success_url = '/projects/{{project_id}}'.replace('{{project_id}}', project_id)
        return context

    def post(self, request, *args, **kwargs):
        project_id = self.kwargs.get('project_id')
        self.success_url = '/projects/{{project_id}}'.replace('{{project_id}}', project_id)
        return super(ReleaseCreate, self).post(self, request, *args, **kwargs)


class ReleaseUpdate(UpdateView):

    model = Release
    # template_name = 'edit.html'
    form_class = forms.ReleaseForm
    success_url = '/releases/'


def release_delete(request, pk):
    Release.objects.filter(id=pk).delete()
    return http.HttpResponseRedirect('/projects/')


#
#   Items
#


class ItemIndex(ListView):
    model = Item
    template_name = 'item_index.html'


class ItemDetail(DetailView):

    model = Item
    template_name = 'item_view.html'

    def get_context_data(self, **kwargs):
        context = super(ItemDetail, self).get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        release_id = self.kwargs.get('release_id')
        context['project_id'] = project_id
        context['release_id'] = release_id
        return context


class ItemCreate(CreateView):

    model = Item
    template_name = 'item_edit.html'
    form_class = forms.ItemForm
    success_url = '/items/'

    def get_context_data(self, **kwargs):
        context = super(ItemCreate, self).get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        release_id = self.kwargs.get('release_id')
        context['project_id'] = project_id
        context['release_id'] = release_id
        return context

    def get_success_url(self):
        project_id = self.kwargs.get('project_id')
        release_id = self.kwargs.get('release_id')

        if 'submit_and_add' in self.get_form_kwargs().get('data'):
            self.success_url = '/projects/project_id/releases/release_id/items/create/'.replace('project_id', project_id).replace('release_id', release_id)
            return self.success_url
        else:
            self.success_url = '/projects/project_id/releases/release_id'.replace('project_id', project_id).replace('release_id', release_id)
            return self.success_url


class ItemUpdate(UpdateView):

    model = Item
    template_name = 'item_edit.html'
    form_class = forms.ItemForm
    success_url = '/items/'

    def get_success_url(self):
        if 'submit_and_add' in self.get_form_kwargs().get('data'):
            return '/items/create/'
        else:
            return self.success_url


def item_delete(request, pk):
    Item.objects.filter(id=pk).delete()
    return http.HttpResponseRedirect('/projects/')


#
#   other stuff
#


from django import template
register = template.Library()

@register.filter('field_class')
def field_class(ob):
    return ob.__class__.__name__






