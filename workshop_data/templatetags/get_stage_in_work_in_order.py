from django import template

register = template.Library()

from workshop_data.models.order import Order
from workshop_data.models.stage_manufacturing_detail_in_work import StageManufacturingDetailInWork
from workshop_data.services.services import get_stage_in_work, get_time_of_work
from sign.models import User

@register.simple_tag
def get_stage_in_work_tag(user, batch_id, operations):
    return get_stage_in_work(user, batch_id, operations).job_is_done

@register.simple_tag
def get_time_of_work_tag(user, batch_id, operations):
    return get_time_of_work(user, batch_id, operations)
