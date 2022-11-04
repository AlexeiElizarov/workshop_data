from django import template

register = template.Library()

from workshop_data.models.order import Order
from workshop_data.models.stage_manufacturing_detail_in_work import StageManufacturingDetailInWork
from workshop_data.services.services import get_stage_in_work
from sign.models import User

@register.simple_tag
def get_stage_in_work_tag(username, batch, operations):
    return get_stage_in_work(username, batch, operations).job_is_done
