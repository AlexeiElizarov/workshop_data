from django import template

register = template.Library()

from workshop_data.services.services import get_stage_in_work, get_time_of_work

@register.simple_tag
def get_stage_in_work_tag(user, batch_id, operations):
    """Возвращает id StageManufacturungDetailInWork"""
    return get_stage_in_work(user, batch_id, operations).job_is_done

@register.simple_tag
def get_time_of_work_tag(user, batch_id, operations):
    """Возвращает время работы(time_of_work) из StageManufacturungDetailInWork"""
    return get_time_of_work(user, batch_id, operations)
