from django import template

from workshop_data.services import get_cost_per_hour

register = template.Library()

@register.simple_tag
def get_cost_per_hour_tag(order_id):
    """Получает стоимость часа при изготовлнии детали"""
    return get_cost_per_hour(order_id)