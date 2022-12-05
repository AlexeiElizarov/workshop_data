from django.core.exceptions import ObjectDoesNotExist

from workshop_data.models.order import Order

from statistics import mean

from workshop_data.services.general_services import get_stage_in_work


def get_order_by_id(id):
    """Получает Наряд по id"""
    try:
        return Order.objects.get(id=id)
    except ObjectDoesNotExist:
        return None

def get_order_by_user(user_id):
    """Получает Наряды по user"""
    try:
        return Order.objects.filter(user=user_id)
    except ObjectDoesNotExist:
        return None

def get_order_by_user_month(user_id, month):
    """Получает Наряды по user и month"""
    try:
        return Order.objects.filter(user=user_id, month=month)
    except:
        return None


def get_cost_per_hour(order_id):
    """Получает стоимость часа при изготовлнии детали"""
    order = get_order_by_id(order_id)
    try:
        time = get_time_of_work(order.id)
        if time != 0:
            return order.quantity * order.price / time
        else:
            return 0
    except:
        if order.time_of_work_order != 0:
            cost_per_hour = order.quantity * order.price / order.time_of_work_order
            return cost_per_hour
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

def get_all_orders_per_detail_per_worker(product, detail, user): #FIXME
    '''Получает все наряды определенного работника по определенной детали'''
    try:
        orders = Order.objects.filter(user=user.id).\
            filter(product_id=product.id).filter(detail_id=detail.id).exists()
        return orders
    except:
        return None


def get_time_of_work(order):
    """Возвращает время работы(time_of_work) из StageManufacturungDetailInWork или из Order"""
    order = get_order_by_id(order.id)
    try:
        time_of_work = get_stage_in_work(order.user, order.batch.id, order.operations).time_of_work_stage
        return time_of_work
    except:
        return order.time_of_work_order

