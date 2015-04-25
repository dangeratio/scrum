from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.utils import timezone
from django import http
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import context


from projects.models import Project
from projects import forms
from releases.models import Release
from items.models import Item


# usage: raise CustomError('asdf')
class CustomError(Exception):

    def __init__(self, msg="Something went wrong."):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class ProjectIndex(ListView):
    model = Project
    template_name = 'project_index.html'

    releases = Release.objects.all()
    items = Item.objects.all()

    '''
    item_count = []

    for project in Project.objects.all():
        # for each project: count items
        # raise CustomError(project.id)
        item_count[project.id] = Item.objects.filter(sprint_id__project__id=project.id)
    '''

    '''
    contest = Contest.objects.get(pk=contest_id)
    votes   = contest.votes_set.select_related()

    vote_counts = {}

    for vote in votes:
      if not vote_counts.has_key(vote.item.id):
        vote_counts[vote.item.id] = {
          'item': vote.item,
          'count': 0
        }

      vote_counts[vote.item.id]['count'] += 1
    '''

    '''
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')

        return render_to_response(request, self.template_name, {'form': form})
    '''


class ProjectDetail(DetailView):
    model = Project
    template_name = 'project_view.html'

    def get_context_data(self, **kwargs):
        cont = super(ProjectDetail, self).get_context_data(**kwargs)
        cont['now'] = timezone.now()
        return cont


class ProjectCreate(CreateView):
    model = Project
    template_name = 'project_edit.html'
    form_class = forms.ProjectForm
    success_url = '/projects/'


class ProjectUpdate(UpdateView):
    model = Project
    template_name = 'project_edit.html'
    form_class = forms.ProjectForm
    success_url = '/projects/'


def delete(request, pk):
    Project.objects.filter(id=pk).delete()
    return http.HttpResponseRedirect('/projects/')


'''
def create(request):
    if request.method == 'POST':
        form = ProjectCreate.as_view()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/projects/')

    # return render_to_response('project_edit.html', locals(), context_instance=context.RequestContext(request))
    return ProjectCreate.as_view()
'''


from django import template
register = template.Library()

@register.filter('field_class')
def field_class(ob):
    return ob.__class__.__name__






