from workshop_data.models.order import Order
from workshop_data.services import get_time_of_work, get_user
from statistics import mean


def get_order_by_id(id):
    """Получает Наряд по id"""
    return Order.objects.get(id=id)

def get_order_by_user(user_id):
    """Получает Наряды по user"""
    return Order.objects.filter(user=user_id)

def get_order_by_user_month(user_id, month):
    """Получает Наряды по user и month"""
    return Order.objects.filter(user=user_id, month=month)

def get_cost_per_hour(order_id):
    """Получает стоимость часа при изготовлнии детали"""
    order = get_order_by_id(order_id)
    time = get_time_of_work(order.user, order.batch.id, order.operations)
    if time != 0:
        return order.quantity * order.price / time
    else:
        return 0

def get_average_cost_per_hour(user_id):
    """Получает средний заработок работника в час за все время"""
    orders = get_order_by_user(user_id)
    try:
        return round(mean([get_cost_per_hour(order.id) for order in orders]), 2)
    except:
        return '--'

def get_average_cost_per_hour_per_month(user_id, month):
    """Получает средний заработок работника в час за месяц"""
    try:
        orders = get_order_by_user_month(user_id, month)
        return round(mean([get_cost_per_hour(order.id) for order in orders]), 2)
    except:
        return '--'


def get_average_price_orders_per_month(user, month):
    """Получает среднюю расценку по нарядам работника за месяц"""
    try:
        orders = Order.objects.filter(user=user, month=month)
        return round(mean([order.price for order in orders]), 2)
    except:
        return '--'

def get_average_price_orders(user):
    """Получает среднюю расценку по нарядам работника за все время"""
    try:
        orders = Order.objects.filter(user=user)
        return round(mean([order.price for order in orders]),2)
    except:
        return '--'

