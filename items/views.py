from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.utils import timezone
from django import http


# model specific references
from items.models import Item
from items import forms


class ItemDetail(DetailView):

    model = Item
    # template_name = 'Item_view.html'

    def get_context_data(self, **kwargs):
        context = super(ItemDetail, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ItemCreate(CreateView):

    model = Item
    # template_name = 'edit.html'
    form_class = forms.ItemForm
    success_url = '/items/'

    '''
    def clean(self):
        if 'submit_and_add' in self.data:
            # add alert of some sort here
            self.formAlert = "Your item was saved."
            self.form_alert_displayed = 1
            self.success_url = '/items/create/'
    '''


class ItemUpdate(UpdateView):

    model = Item
    # template_name = 'edit.html'
    form_class = forms.ItemForm
    success_url = '/items/'

    def get_success_url(self):
        if 'submit_and_add' in self.get_form_kwargs().get('data'):
            return '/items/create/'
        else:
            return self.success_url


def delete(request, pk):
    Item.objects.filter(id=pk).delete()
    return http.HttpResponseRedirect('/items/')


class CustomError(Exception):

    def __init__(self, msg="Something went wrong."):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)






