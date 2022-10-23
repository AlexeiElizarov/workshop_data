from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import BatchDetailInPlan, Order
from sign.models import User
from collections import OrderedDict


# def replacing_True_False_flag(request):
#     print(request.GET)
#     print(request.GET.kwargs)
#     return HttpResponseRedirect(reverse_lazy('start_new_stage_in_work_complete'))


def batch_ready(request, year, month, id):
    '''Реализует кнопку "Сдача детали" в списке Партий в Плане'''
    batch = BatchDetailInPlan.objects.get(id=id)
    batch.ready = True
    batch.save()
    # return HttpResponseRedirect(reverse_lazy('batch_ready_comlite',kwargs={'year': year, 'month': month, 'id': id}))
    return HttpResponseRedirect(reverse_lazy('batchs_in_plan', kwargs={'object': batch.detail}))

def batch_cancel_ready(request, year, month, id):
    '''Реализует кнопку "Отменя сдачи" в списке Партий в Плане'''
    batch = BatchDetailInPlan.objects.get(id=id)
    batch.ready = False
    batch.save()
    return HttpResponseRedirect(reverse_lazy('batchs_in_plan', kwargs={'object': batch.detail}))

def get_quantity_detail_by_orders(product, detail, user):
    '''Получает все наряды определенного работника по определенной детали'''
    orders = Order.objects.filter(surname=user.id).filter(product_id=product.id).filter(detail_id=detail.id)
    return orders

def get_list_all_workers():
    '''Получает список всех работников'''
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


