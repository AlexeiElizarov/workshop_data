from django import template

register = template.Library()

from workshop_data.services.general_services import (
    return_salary_for_completed_detail,
    return_salary_per_month
    )


@register.simple_tag
def returns_salary_for_completed_detail_tag(record):
    """Возвращает зарплату за сделанные детали. Данные берутся из RecordJob"""
    return return_salary_for_completed_detail(record)

@register.simple_tag
def return_salary_per_month_tag(records):
    """Возвращает зарплату оператора за месяц. Данные берутся из RecordJob"""
    return return_salary_per_month(records)


@register.simple_tag
def month_name_tag(month_number):
    import calendar
    return calendar.month_name[int(month_number)]