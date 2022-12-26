from django import template

from workshop_data.models.order import Order
from workshop_data.services import get_cost_per_hour, get_average_cost_per_hour, get_average_price_orders, \
    get_average_price_orders_per_month, get_average_cost_per_hour_per_month, get_time_of_work

register = template.Library()

from workshop_data.services.general_services import get_stage_in_work, get_time_of_work


@register.simple_tag
def get_stage_in_work_done_tag(order, user, batch_id, operations):
    """Возвращает job_is_done StageManufacturungDetailInWork"""
    try:
        job_is_done = get_stage_in_work(user, batch_id, operations).job_is_done
        return job_is_done
    except:
        return 'нет этапа'#Order.objects.get(id=order.id).operations


@register.simple_tag
def get_cost_per_hour_tag(order_id):
    """Тэг стоимость часа при изготовлении определённой детали"""
    return get_cost_per_hour(order_id)


@register.simple_tag
def get_average_cost_per_hour_tag(user_id):
    """Тэг средний заработок работника в час"""
    return get_average_cost_per_hour(user_id)


@register.simple_tag
def get_average_cost_per_hour_per_month_tag(user_id, month):
    """Тэг средний заработок работника в час за месяц"""
    return get_average_cost_per_hour_per_month(user_id, month)


@register.simple_tag
def get_average_price_orders_tag(user):
    """Тэг средняя расценка по нарядам за все время"""
    return get_average_price_orders(user)


@register.simple_tag
def get_average_price_orders_per_month_tag(user, month):
    """Тэг средняя расценка по нарядам работника за месяц"""
    return get_average_price_orders_per_month(user, month)


@register.simple_tag
def get_time_of_work_stage_or_order_tag(id):
    """Возвращает время работы"""
    try:
        time = get_time_of_work(id)
        return time
    except:
        return '--'
