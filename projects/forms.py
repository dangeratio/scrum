from django import forms
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


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project

        fields = '__all__'


class ReleaseForm(forms.ModelForm):

    class Meta:
        model = Release

        fields = '__all__'


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




