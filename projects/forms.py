from django import forms
from models import Project


# for custom select widget
from django.utils.html import mark_safe, escape, conditional_escape
from django.utils.encoding import force_unicode
from django.forms.widgets import flatatt
from itertools import chain
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


class SelectWidgetBootstrap(forms.Select):
    """
    http://twitter.github.com/bootstrap/components.html#buttonDropdowns
    Needs bootstrap and jquery
    """
    js = ("""
    <script type="text/javascript">
        function setBtnGroupVal(elem) {
            btngroup = $(elem).parents('.main-identifier');
            selected_a = btngroup.find('a[selected]');
            if (selected_a.length > 0) {
                val = selected_a.attr('data-value');
                label = selected_a.html();
            } else {
                btngroup.find('a').first().attr('selected', 'selected');
                setBtnGroupVal(elem);
            }
            btngroup.find('input').val(val);
            btngroup.find('.dropdown-identifier').html(label);
        }
        $(document).ready(function() {
            $('.main-identifier input').each(function() {
                setBtnGroupVal(this);
            });
            $('.ul-identifier li a').click(function() {
                $(this).parent().siblings().find('a').attr('selected', false);
                $(this).attr('selected', true);
                setBtnGroupVal(this);
            });
            $('label[for=id_owner]').addClass('full-width');
        })
    </script>
    """)

    def __init__(self, attrs={'class': 'btn-group noborder-fix main-identifier'}, choices=()):
        self.noscript_widget = forms.Select(attrs={}, choices=choices)
        super(SelectWidgetBootstrap, self).__init__(attrs, choices)

    def __setattr__(self, k, value):
        super(SelectWidgetBootstrap, self).__setattr__(k, value)
        if k != 'attrs':
            self.noscript_widget.__setattr__(k, value)

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = ["""<div%(attrs)s>"""
                  """    <button class="btn btn-default dropdown-toggle dropdown-identifier" data-toggle="dropdown" type="button">%(label)s"""
                  """    </button>"""
                  """    <ul class="dropdown-menu ul-identifier">"""
                  """        %(options)s"""
                  """    </ul>"""
                  """    <input type="hidden" name="%(name)s" value="" class="btn-group-value" />"""
                  """</div>"""
                  """%(js)s"""
                  """<noscript>%(noscript)s</noscript>"""
                   % {'attrs': flatatt(final_attrs),
                      'options': self.render_options(choices, [value]),
                      'label': _(u'None'),
                      'name': name,
                      'js': SelectWidgetBootstrap.js,
                      'noscript': self.noscript_widget.render(name, value, {}, choices)} ]
        return mark_safe(u'\n'.join(output))

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_unicode(option_value)
        selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
        return u'<li><a href="javascript:void(0)" data-value="%s"%s>%s</a></li>' % (
            escape(option_value), selected_html,
            conditional_escape(force_unicode(option_label)))

    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set([force_unicode(v) for v in selected_choices])
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<li class="divider" label="%s"></li>' % escape(force_unicode(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return u'\n'.join(output)


class ProjectForm(forms.ModelForm):

    '''
    owner = forms.ModelChoiceField(User.objects.all(),
                                   widget=SelectWidgetBootstrap(),
                                   empty_label=u'None',
                                   required=False,
                                   )
    '''

    class Meta:
        model = Project

        fields = (
            'title',
            'detail',
            'owner',
            'key_title',
        )