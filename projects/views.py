from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.utils import timezone
from django import http


from projects.models import Project
from projects import forms
from releases.models import Release
from items.models import Item


class ProjectIndex(ListView):
    model = Project



class ProjectDetail(DetailView):

    model = Project
    # template_name = 'project_view.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ProjectCreate(CreateView):

    model = Project
    # template_name = 'edit.html'
    form_class = forms.ProjectForm
    success_url = '/projects/'


class ProjectUpdate(UpdateView):

    model = Project
    # template_name = 'edit.html'
    form_class = forms.ProjectForm
    success_url = '/projects/'


def delete(request, pk):
    Project.objects.filter(id=pk).delete()
    return http.HttpResponseRedirect('/projects/')


from django import template
register = template.Library()

@register.filter('field_class')
def field_class(ob):
    return ob.__class__.__name__





