from django import forms
from django.core.exceptions import PermissionDenied
from django.forms import widgets
from projects.models import Project, Release, Item

# for custom select widget
'''
from django.utils.html import mark_safe, escape, conditional_escape
from django.utils.encoding import force_unicode
from django.forms.widgets import flatatt
from itertools import chain
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
'''


# usage: raise DebugMessage('asdf')
class DebugMessage(Exception):

    def __init__(self, msg="Something went wrong."):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project

        fields = '__all__'


class ReleaseForm(forms.ModelForm):

    class Meta:
        model = Release

        fields = '__all__'

    def clean_title(self):
        data = self.cleaned_data['title']

        if "backlog" in data:
            raise forms.ValidationError("You cannot have backlog in a release title.")

        # Always return the cleaned data, whether you have changed it or
        # not.
        return data



class ItemForm(forms.ModelForm):

    class Meta:
        model = Item

        fields = '__all__'

        exclude = (
            'key',
        )

        '''
        widgets = {
            'priority': forms.widgets.RadioChoiceInput(),
        }
        '''




