from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.utils import timezone
from django import http


from releases.models import Release
from releases import forms


class ReleaseDetail(DetailView):

    model = Release
    # template_name = 'view.html'

    def get_context_data(self, **kwargs):
        context = super(ReleaseDetail, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ReleaseIndex(CreateView):

    model = Release
    # template_name = 'edit.html'
    form_class = forms.ReleaseForm
    success_url = '/releases/'


class ReleaseUpdate(UpdateView):

    model = Release
    # template_name = 'edit.html'
    form_class = forms.ReleaseForm
    success_url = '/releases/'


def delete(request, pk):
    Release.objects.filter(id=pk).delete()
    return http.HttpResponseRedirect('/releases/')













