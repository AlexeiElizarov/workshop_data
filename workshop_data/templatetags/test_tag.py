from django import template

register = template.Library()

@register.simple_tag
def button_tag():
    print('***_***_***')
