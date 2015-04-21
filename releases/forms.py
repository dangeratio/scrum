from django import forms
from models import Release


class ReleaseForm(forms.ModelForm):

    class Meta:
        model = Release

        fields = '__all__'

        '''
        fields = (
            'title',
            'detail',
            'number',
            'status',
            'start_date',
            'release_date',
            'project_id',
        )
        '''
