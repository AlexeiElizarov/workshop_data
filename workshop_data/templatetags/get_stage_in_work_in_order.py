from django import template

from workshop_data.models.order import Order

register = template.Library()

from workshop_data.services.general_services import get_stage_in_work

@register.simple_tag
def get_stage_in_work_done_tag(order, user, batch_id, operations):
    """Возвращает job_is_done StageManufacturungDetailInWork"""
    try:
        job_is_done = get_stage_in_work(user, batch_id, operations).job_is_done
        return job_is_done
    except:
        return Order.objects.get(id=order.id).operations

# @register.simple_tag
# def get_time_of_work_stage_tag(order):
#     """Возвращает время работы(time_of_work) из StageManufacturungDetailInWork"""
#     try:
#         time = get_time_of_work(order)
#         return time
#     except:
#         return '--'
