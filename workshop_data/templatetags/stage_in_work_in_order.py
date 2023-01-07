from django import template

register = template.Library()


@register.simple_tag
def get_time_for_work_quantity_detail_tag(time, quantity):
    """Получает общее время производства определенного количества деталей"""
    return round((float(time) * float(quantity)), 2)
