from workshop_data.models.order import Order
from workshop_data.services import get_time_of_work


def get_order(id):
    """Получает Наряд по id"""
    return Order.objects.get(id=id)

def get_cost_per_hour(order_id):
    """Получает стоимость часа при изготовлнии детали"""
    order = get_order(order_id)
    return order.quantity * order.price / get_time_of_work(order.surname, order.batch.id, order.operations)
