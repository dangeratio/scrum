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


class ProjectIndex(ListView):
    model = Project
    template_name='project_index.html'

class ProjectDetail(DetailView):
    model = Project
    template_name='project_view.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


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





