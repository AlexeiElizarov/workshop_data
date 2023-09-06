from django import template

register = template.Library()

from workshop_data.services.general_services import (
    return_salary_for_completed_detail
    )


@register.simple_tag
def returns_salary_for_completed_detail_tag(record):
    """Возвращает зарплату за сделанные детали. Данные берутся из RecordJob"""
    return return_salary_for_completed_detail(record)
