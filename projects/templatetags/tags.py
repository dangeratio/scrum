#   custom template tags
#

from projects.models import Item
from django import template


register = template.Library()


# usage: raise DebugMessage('asdf')
class DebugMessage(Exception):

    def __init__(self, msg="Something went wrong."):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


@register.filter('field_class')
def field_class(ob):
    return ob.__class__.__name__


@register.filter('show_priority')
def show_priority(ob):
    # Item.PRIORITY_CHOICES[ob][0] = the number (IE: 3)
    # Item.PRIORITY_CHOICES[ob][1] = the text value (IE: Medium)

    # raise DebugMessage(Item.PRIORITY_CHOICES[ob-1])

    if ob:
        return Item.PRIORITY_CHOICES[ob - 1][1]
    else:
        return 'None'


@register.filter('priority_css')
def priority_css(ob):
    # Item.PRIORITY_CHOICES[ob][0] = the number (IE: 3)
    # Item.PRIORITY_CHOICES[ob][1] = the text value (IE: Medium)
    # return Item.PRIORITY_CHOICES[ob][0]

    css = 'default'

    if ob == 1:
        css = 'success'
    elif ob == 2:
        css = 'success'
    elif ob == 3:
        css = 'warning'
    elif ob == 4:
        css = 'warning'
    elif ob == 5:
        css = 'danger'

    return css


@register.filter('return_value')
def return_value(obj, arg):
    # raise DebugMessage(ob)
    return obj[arg]


class SetVarNode(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""


def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return SetVarNode(parts[1], parts[3])

register.tag('set', set_var)


@register.filter('percent')
def percentage(value):
    return '{0:.2%}'.format(value)


@register.filter('status')
def status(value):
    return Item.STATUS_CHOICES[value-1][1]

