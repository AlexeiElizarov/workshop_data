import datetime

from django.core.validators import MaxValueValidator
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from sign.models import User
from workshop_data.models.statement_about_job_over_detail import ResolutionForStatementAboutJobOverDetail, \
    StatementAboutJobOverDetail
from workshop_data.models.batch_detail_in_plan import BatchDetailInPlan
from workshop_data.models.stage_manufacturing_detail_in_work import StageManufacturingDetailInWork
from workshop_data.models.stage_manufacturing_detail import StageManufacturingDetail
from workshop_data.models.bonus import Bonus
from django.core.exceptions import ObjectDoesNotExist
from workshop_data.models.order import Order
from statistics import mean


def current_year():
    return datetime.date.today().year


def current_month():
    return datetime.date.today().month


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


def get_current_user(request):
    return request.user


def get_stage_in_work(user, batch_id, operations):
    """Возвращает id StageManufacturingDetailInWork по username, batch, operations"""
    try:
        batch = BatchDetailInPlan.objects.get(id=batch_id)
        # worker = User.objects.get(username=user)
        stage_in_batch_id = StageManufacturingDetail.objects.get(
            detail_id=batch.workshopplan_detail.detail, operations=operations.split()[0]
        )
        stage = StageManufacturingDetailInWork.objects.get(
            worker=get_user_by_username(user), batch=batch, stage_in_batch_id=stage_in_batch_id
        )
        return stage
    except ObjectDoesNotExist:
        return None


def stage_in_work_ready(request, username, batch, operations):
    """Реализует "Выполнено" в таблице Наряды(для Работника)"""
    stage = get_stage_in_work(username, batch, operations)
    stage.job_is_done = False if stage.job_is_done == True else True
    stage.save()
    return HttpResponseRedirect(reverse_lazy('orders_user_month_list',
                                             kwargs={'month': current_month(), 'username': username}))


def resolution_statement_about_job_over_detail(request, id, username):
    """Реализует одобрение или нет заявления на работу с Деталью"""
    statement = StatementAboutJobOverDetail.objects.get(id=id)
    resolute = statement.resolute.first()
    resolute.resolution = True if resolute.resolution == False else True
    resolute.master = User.objects.get(username=username)
    resolute.date_approval = datetime.date.today()
    resolute.save()
    return HttpResponseRedirect(reverse_lazy('list_all_resolution_or_not_detail',
                                             kwargs={'username': username}))


def batch_ready(request, year, month, id):
    """Реализует кнопку "Сдача детали" в списке Партий в Плане"""
    batch = BatchDetailInPlan.objects.get(id=id)
    batch.ready = True
    batch.save()
    # return HttpResponseRedirect(reverse_lazy('batch_ready_comlite',kwargs={'year': year, 'month': month, 'id': id}))
    return HttpResponseRedirect(reverse_lazy('batchs_in_plan', kwargs={'object': batch.workshopplan_detail}))


def batch_cancel_ready(request, year, month, id):
    """Реализует кнопку "Отменя сдачи" в списке Партий в Плане"""
    batch = BatchDetailInPlan.objects.get(id=id)
    batch.ready = False
    batch.save()
    return HttpResponseRedirect(reverse_lazy('batchs_in_plan', kwargs={'object': batch.workshopplan_detail}))


def get_list_all_workers_initials():
    """Получает список всех работников(ФИО)"""
    lst = [worker.surname for worker in User.objects.all()]
    return lst


def get_user(user_id):
    """Получает пользователя по id"""
    return get_object_or_404(User, id=user_id)


def get_user_by_username(username):
    """Получает user по username"""
    return get_object_or_404(User, username=username)


def get_list_all_workers():
    """Получает список всех работников(username)"""
    return User.objects.filter(position__in=['LSM', 'TRN', 'MLR'])


def get_list_locksmith():
    """Получает список всех слесарей"""
    return User.objects.filter(position='LSM')


def get_list_turner():
    """Получает список всех токарей"""
    return User.objects.filter(position='TRN')


def get_list_miller():
    """Получает список всех фрезеровщиков"""
    return User.objects.filter(position='MLR')


def get_dict_worker_quantity_detail(product, detail, workers) -> dict:
    """
    Получает количество определенных деталей у всех работников из списка.
    Возвращает словарь {worker: quantity}
    """
    dict_workers_quantity = {}
    for worker in workers:
        quantity = 0
        dict_workers_quantity[worker.surname] = quantity
        for order in get_all_orders_per_detail_per_worker(product, detail, worker):
            dict_workers_quantity[worker.surname] += order.quantity
    return dict_workers_quantity


def get_quantity_detail(worker, product, detail):
    """Получает количество деталей по определенным нарядам"""
    return get_all_orders_per_detail_per_worker(worker, product, detail).aggregate(Sum('quantity'))['quantity__sum']


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
    """Получает стоимость часа при изготовлении детали"""
    order = get_order_by_id(order_id)
    time = get_time_of_work(order_id)
    if time != 0:
        cost_per_hour = order.quantity * order.price / time
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
        return round(mean([order.price for order in orders]), 2)
    except:
        return '--'


def get_all_orders_per_detail_per_worker(product, detail, user):  # FIXME
    """Получает все наряды определенного работника по определенной детали"""
    try:
        orders = Order.objects.filter(user=user.id). \
            filter(product_id=product.id).filter(detail_id=detail.id)
        return orders
    except:
        return 0


def get_time_of_work(id):
    """Возвращает время работы(time_of_work) из StageManufacturingDetailInWork или из Order"""
    order = get_order_by_id(id)
    try:
        time_of_work = get_stage_in_work(order.user, order.batch.id, order.operations).time_of_work_stage
        return time_of_work
    except:
        return order.time_of_work_order


def get_all_bonuses_per_month(user, month):
    """Возвращает общую премию рабочего за определённый месяц"""
    bonuses = Bonus.objects.filter(worker=user, month=month)
    if Bonus.objects.filter(worker=user, month=13).exists():
        return 'Редактировать'
    return bonuses.aggregate(Sum('quantity'))['quantity__sum']
