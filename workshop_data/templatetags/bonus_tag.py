from django import template

from workshop_data.services import get_all_bonuses_per_month

register = template.Library()


@register.simple_tag
def get_all_bonuses_per_month_tag(user, month):
    """Тэг возвращает общую премию рабочего за определённый месяц"""
    return get_all_bonuses_per_month(user, month)
