from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, ModelFormMixin, DeleteView
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

    def get_context_data(self, **kwargs):
        context = super(ProjectIndex, self).get_context_data(**kwargs)
        total_projects = Project.objects.all().count()
        total_releases = Release.objects.all().count()
        total_items = Item.objects.all().count()
        context['total_projects'] = total_projects
        context['total_releases'] = total_releases
        context['total_items'] = total_items
        return context


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

    def form_valid(self, form):

        # create the project object and save it
        self.object = form.save()
        created_project_id = self.object.id

        # create a "backlog" release to start out with
        backlog = Release.objects.create(
            project_id=created_project_id,
            title='Backlog',
            detail='The default backlog group',
        )
        backlog.save()

        return super(ModelFormMixin, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        project_id = ''
        self.success_url = '/projects/project_id'.replace("project_id", project_id)
        return super(ProjectCreate, self).post(request, *args, **kwargs)


class ProjectCreateQuick(ProjectCreate):

    template_name = 'project_quick.html'

    def form_valid(self, form):

        # create the project object and save it
        self.object = form.save()
        created_project_id = self.object.id

        # create a "backlog" release to start out with
        backlog = Release.objects.create(
            project_id=created_project_id,
            title='Backlog',
            detail='The default backlog group',
        )
        backlog.save()
        backlog_object_id = backlog.pk

        # backlog_object_id = backlog_object.id

        # create sub items under the backlog
        quick_items = self.request.POST['quick_items']
        for lines in iter(quick_items.splitlines()):
            values = lines.split(',')
            new_item = Item.objects.create(
                release_id=backlog_object_id,
                title=values[0],
                detail=values[1],
            )
            new_item.save()

        return super(ModelFormMixin, self).form_valid(form)




class ProjectUpdate(UpdateView):
    model = Project
    template_name = 'project_edit.html'
    form_class = forms.ProjectForm
    success_url = '/projects/'
    slug_field = 'project_id'


'''
def project_delete(request, pk):
    Project.objects.filter(pk=pk).delete()
    slug_field = 'project_id'
    return http.HttpResponseRedirect('/projects/')
'''


class ProjectDelete(DeleteView):

    model = Project
    template_name = 'project_delete.html'
    form_class = forms.ProjectForm
    success_url = '/projects/'



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
    template_name='release_view.html'

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
    template_name='release_edit.html'

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
    template_name='release_edit.html'


class ReleaseDelete(DeleteView):

    model = Release
    form_class = forms.ReleaseForm
    template_name='release_delete.html'

    def get_context_data(self, **kwargs):
        context = super(ReleaseDelete, self).get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        context['project_id'] = project_id
        return context

    def get_success_url(self):
        project_id = self.kwargs.get('project_id')
        success_url = '/projects/{{project_id}}'.replace('{{project_id}}', project_id)
        return success_url


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


'''
def item_delete(request, pk):
    Item.objects.filter(id=pk).delete()
    return http.HttpResponseRedirect('/projects/')
'''


class ItemDelete(DeleteView):

    model = Item
    form_class = forms.ItemForm
    template_name = 'item_delete.html'

    def get_context_data(self, **kwargs):
        context = super(ItemDelete, self).get_context_data(**kwargs)
        project_id = self.kwargs.get('project_id')
        release_id = self.kwargs.get('release_id')
        item_id = self.kwargs.get('pk')
        context['project_id'] = project_id
        context['release_id'] = release_id
        context['item_id'] = item_id
        return context

    def get_success_url(self):
        project_id = self.kwargs.get('project_id')
        release_id = self.kwargs.get('release_id')
        success_url = '/projects/project_id/releases/release_id'.replace('project_id', project_id).replace('release_id', release_id)
        return success_url


#
#   other stuff
#


from django import template
register = template.Library()

@register.filter('field_class')
def field_class(ob):
    return ob.__class__.__name__






