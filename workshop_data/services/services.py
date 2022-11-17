import datetime

from django.core.validators import MaxValueValidator
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from sign.models import User
from workshop_data.models.batch_detail_in_plan import BatchDetailInPlan
from workshop_data.models.order import Order
from workshop_data.models.stage_manufacturing_detail_in_work import StageManufacturingDetailInWork
from workshop_data.models.stage_manufacturing_detail import StageManufacturingDetail


def current_year():
    return datetime.date.today().year

def current_month():
    return datetime.date.today().month

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

def get_current_user(request):
    return request.user

def get_stage_in_work(user, batch_id, operations):
    '''Возвращает id StageManufacturungDetailInWork по username, batch, operations'''
    batch = BatchDetailInPlan.objects.get(id=batch_id)
    worker = User.objects.get(username=user)
    stage_in_batch_id = StageManufacturingDetail.objects.get(
        detail_id=batch.workshopplan_detail.detail, operations=operations.split()[0]
    )
    stage = StageManufacturingDetailInWork.objects.get(
        worker=worker, batch=batch_id, stage_in_batch_id=stage_in_batch_id
    )
    return stage

def get_time_of_work(user, batch_id, operations):
    """Возвращает время работы(time_of_work) из StageManufacturungDetailInWork"""
    return get_stage_in_work(user, batch_id, operations).time_of_work

def stage_in_work_ready(request, username, batch, operations):
    '''Реализует "Выполнено" в таблице Наряды(для Работника)'''
    stage = get_stage_in_work(username, batch, operations)
    stage.job_is_done = False if stage.job_is_done == True else True
    stage.save()
    return HttpResponseRedirect(reverse_lazy('orders_user_month_list',
                                             kwargs={'month': current_month(), 'username': username}))

def batch_ready(request, year, month, id):
    '''Реализует кнопку "Сдача детали" в списке Партий в Плане'''
    batch = BatchDetailInPlan.objects.get(id=id)
    batch.ready = True
    batch.save()
    # return HttpResponseRedirect(reverse_lazy('batch_ready_comlite',kwargs={'year': year, 'month': month, 'id': id}))
    return HttpResponseRedirect(reverse_lazy('batchs_in_plan', kwargs={'object': batch.workshopplan_detail}))

def batch_cancel_ready(request, year, month, id):
    '''Реализует кнопку "Отменя сдачи" в списке Партий в Плане'''
    batch = BatchDetailInPlan.objects.get(id=id)
    batch.ready = False
    batch.save()
    return HttpResponseRedirect(reverse_lazy('batchs_in_plan', kwargs={'object': batch.workshopplan_detail}))

def get_quantity_detail_by_orders(product, detail, user):
    '''Получает все наряды определенного работника по определенной детали'''
    orders = Order.objects.filter(surname=user.id).\
        filter(product_id=product.id).filter(detail_id=detail.id)
    return orders

def get_list_all_workers_initials():
    '''Получает список всех работников(ФИО)'''
    lst = [worker.surname for worker in User.objects.all()]
    print(lst)
    return lst

def get_list_all_workers():
    '''Получает список всех работников(username)'''
    return User.objects.filter(position__in=['LSM', 'TRN', 'MLR'])

def get_list_locksmith():
    '''Получает список всех слесарей'''
    return User.objects.filter(position='LSM')

def get_list_turner():
    '''Получает список всех токарей'''
    return User.objects.filter(position='TRN')

def get_list_miller():
    '''Получает список всех фрезеровщиков'''
    return User.objects.filter(position='MLR')

def get_dict_worker_quantity_detail(product, detial, workers) -> dict:
    '''
    Получает колличество определенных деталей у всех работников из списка.
    Возвращает словарь {worker: quantity}
    '''
    dict_workers_quantity = {}
    for worker in workers:
        quantity = 0
        dict_workers_quantity[worker.surname] = quantity
        for order in get_quantity_detail_by_orders(product, detial, worker):
            dict_workers_quantity[worker.surname] += order.quantity
    return dict_workers_quantity

def get_quantity_detail(worker, product, detail):
    '''Получает колличество деталей по определеным нарядам'''
    return get_quantity_detail_by_orders(worker, product, detail).aggregate(Sum('quantity'))['quantity__sum']



