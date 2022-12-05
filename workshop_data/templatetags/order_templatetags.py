from django import template

from workshop_data.services import get_cost_per_hour, get_average_cost_per_hour, get_average_price_orders, \
    get_average_price_orders_per_month, get_average_cost_per_hour_per_month, get_time_of_work

register = template.Library()


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
def get_time_of_work_stage_or_order_tag(order):
    """Возвращает время работы(time_of_work) из StageManufacturungDetailInWork"""
    try:
        time = get_time_of_work(order)
        return time
    except:
        return '--'
