from django import template

from workshop_data.models import DetailDetail

register = template.Library()


@register.simple_tag
def total_count(initial=None, _count=[0]):  # noqa
    if initial is not None:
        # reset counter and make sure nothing is printed
        _count[0] = initial
        return ''
    # increment counter
    _count[0] += 1
    return _count[0]


@register.filter
def detail_in(var, detail):
    return DetailDetail.objects.filter(main_detail=detail)


@register.simple_tag
def get_verbose_field_name_tag(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.get_field(field_name).verbose_name.title()