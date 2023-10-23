import datetime
from typing import Union

from django.core.validators import MaxValueValidator
from django.db.models import Sum, F
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from sign.models import User
from workshop_data.models import Detail
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


def get_stage_in_work(order: Order) -> Union[StageManufacturingDetailInWork or None]:
    """Возвращает StageManufacturingDetailInWork по username, batch, operations"""
    try:
        batch = BatchDetailInPlan.objects.get(id=order.batch).select_related('workshopplan_detail')
        stage_in_batch_id = StageManufacturingDetail.objects.get(
            detail_id=order.detail, operations=order.operations.split()[0]
        )
        stage = StageManufacturingDetailInWork.objects.get(
            worker=get_user_by_username(order.user), batch=batch, stage_in_batch_id=stage_in_batch_id
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
    return User.objects.filter(position__in=['866', '914', '944', '916', '892', '961', '773', '601'])


def get_list_locksmith():
    """Получает список всех слесарей"""
    return User.objects.filter(position='866') | User.objects.filter(employee_number__in=[130, 400])


def get_list_turner():
    """Получает список всех токарей"""
    miller_list = User.objects.none()
    miller_list = miller_list | User.objects.filter(position='914')
    return miller_list


def get_list_miller():
    """Получает список всех фрезеровщиков"""
    return User.objects.filter(position='944') | User.objects.filter(employee_number__in=[21, 252])


def get_list_operator():
    """Получает список всех операторов"""
    return User.objects.filter(position='773')


def get_batch_by_id(batch_id):
    """Получает объект Партия по id"""
    return get_object_or_404(BatchDetailInPlan, id=batch_id)


def get_dict_worker_quantity_detail(product, detail, workers) -> dict:
    """
    Получает количество определенных деталей у всех работников из списка.
    Возвращает словарь {worker: quantity}
    """
    dict_workers_quantity = {}
    for worker in workers:
        dict_workers_quantity[worker.surname] = 0
        dict_workers_quantity[worker.surname] += \
            get_all_orders_per_detail_per_worker_unigue_batch(product, detail, worker)
    return dict_workers_quantity


def get_quantity_detail(worker, product, detail):
    """Получает количество деталей по определенным нарядам"""
    return get_all_orders_per_detail_per_worker(worker, product, detail).aggregate(Sum('quantity'))['quantity__sum']


def get_order_by_id(order_id: int) -> Union[Order, None]:
    """Получает Наряд по id"""
    try:
        return Order.objects.get(id=order_id)
    except ObjectDoesNotExist:
        return None


def get_order_by_batch_user_operations(batch_id, worker, operations):
    """Получает наряд по batch_id, worker, operations"""
    try:
        return Order.objects.get(batch=batch_id, user=worker.id, operations=operations)
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


def get_cost_per_hour(order: Order) -> float:
    """Получает стоимость часа при изготовлении детали"""
    time = order.time_of_work_order
    if time != 0:
        if order.price:
            return round(order.quantity * order.price / time, 2) / 100
        elif order.stage.price:
            return round(order.quantity * order.stage.price / time, 2) / 100
    else:
        return 0


def get_average_cost_per_hour(orders):
    """Получает средний заработок работника по нарядам в час за все время"""
    # orders = Order.objects.filter(user=worker)
    try:
        return round(mean([get_cost_per_hour(order) for order in orders]), 2)
    except:
        return '--'


def get_average_cost_per_hour_per_month(orders):
    """Получает средний заработок работника в час за месяц"""
    try:
        return round(mean([get_cost_per_hour(order.id) for order in orders]), 2)
    except:
        return '--'


def get_average_price_orders_per_month(orders):
    """Получает среднюю расценку по нарядам работника за месяц"""
    try:
        return round(mean([order.price for order in orders]), 2)
    except:
        return '--'


def get_average_price_orders(orders):
    """Получает среднюю расценку по нарядам работника за все время"""
    try:
        return round(mean([order.price for order in orders]), 2)
    except:
        return '--'


def get_all_orders_per_detail_per_worker(product, detail, user):
    """Получает все наряды определенного работника по определенной детали"""
    try:
        orders = Order.objects.filter(user=user.id). \
            filter(product_id=product.id).filter(detail_id=detail.id)
        return orders
    except:
        return 0


def get_all_orders_per_detail_per_worker_unigue_batch(product, detail, user):
    """Получает количество деталей определенного работника по определенной детали учитывая уникальность партии"""
    try:
        orders = Order.objects.filter(user=user.id). \
            filter(product_id=product.id).filter(detail_id=detail.id). \
            order_by('date')
        quantity = 0
        batch = []
        for order in orders:
            if order.batch not in batch:
                quantity += order.quantity
                batch.append(order.batch)
        return quantity
    except:
        return 0


def get_average_time_of_work_stage_in_detail(detail):
    """Получает среднее время работы определённого этапа производства детали (общее)"""
    try:
        stages_and_time = {}
        for stage in StageManufacturingDetail.objects.filter(detail=Detail.objects.get(name=detail)):
            try:
                stages_and_time[stage] = \
                    round(mean(
                        [order.time_of_work_order / order.quantity for order in Order.objects.filter(operations=stage)]
                    ) / 8, 8)
            except:
                stages_and_time[stage] = 0
        return stages_and_time
    except:
        return None


def get_average_time_of_work_stage_in_detail_per_worker(worker, product, detail, operations):
    """Получает среднее время работы определённого этапа производства детали у рабочего"""
    try:
        for operation in operations:
            orders = Order.objects.filter(
                user=worker.id, product_id=product.id, detail_id=detail.id, operations=operation)
            average_time_of_work = sum([order.time_of_work_order for order in orders])
            return round(mean(average_time_of_work), 2)
    except:
        return 0


def get_time_of_work(order: Order):
    """Возвращает время работы(time_of_work) из StageManufacturingDetailInWork или из Order"""
    try:  # Fixme
        time = order.time_of_work_order
        return time if time > 0 else '--'
    except:
        return 'error'


def get_all_bonuses_per_month(user, month):
    """Возвращает общую премию рабочего за определённый месяц"""
    bonuses = Bonus.objects.filter(worker=user, month=month)
    if Bonus.objects.filter(worker=user, month=13).exists():
        return 'Редактировать'
    sum = bonuses.aggregate(Sum('quantity'))['quantity__sum']
    if sum is None:
        return '--'
    else:
        return sum


def get_not_work_stages_in_batch(batch):
    """Возвращает оставшиеся этапы Партии(не выполненные)"""
    stages_in_work = StageManufacturingDetailInWork.objects.filter(batch_id=batch.id)
    stages_all = batch.workshopplan_detail.detail.stages_detail.all()
    not_work_stages = []
    for i in range(len(stages_in_work), len(stages_all)):
        not_work_stages.append(stages_all[i])
    return not_work_stages


def return_salary_for_completed_detail(record):
    """Возвращает зарплату за сделанные детали. Данные берутся из RecordJob"""
    try:
        if record.quantity == 0 or record.quantity is None:
            time_1 = record.detail.parameters_for_spu.first_side_time
            time_2 = record.detail.parameters_for_spu.second_side_time
            time = time_1 + time_2
            quantity_1 = 0 if record.quantity_1 is None else record.quantity_1
            quantity_2 = 0 if record.quantity_2 is None else record.quantity_2
            price = record.detail.parameters_for_spu.price
            salary_per_minute = price / time
            coefficient_1 = record.detail.parameters_for_spu.coefficient_first_side
            coefficient_2 = record.detail.parameters_for_spu.coefficient_second_side
            salary = quantity_1 * time_1 / time * price * coefficient_1 + \
                     quantity_2 * time_2 / time * price * coefficient_2
            salary = salary * 1.4
            return round(salary, 2)
        elif record.quantity > 0:
            salary = record.quantity * record.detail.parameters_for_spu.price * 1.4
            return round(salary, 2)
    except:
        return '???'


def return_salary_per_month(records):
    """Возвращает зарплату оператора за месяц"""
    salary = []
    try:
        for record in records:
            salary.append(return_salary_for_completed_detail(record))
        return round(sum(salary), 2)
    except:
        return '???'


def return_sum_recordjob_every_detail(records):
    """Возвращает общее количество деталей по одинаковым записям за месяц(определенного рабочего)"""
    try:
        dict = {}
        for record in records:
            detail = f'{record.product} {record.detail}'
            quantity = record.quantity if record.quantity else 0
            quantity_1 = record.quantity_1 if record.quantity_1 else 0
            quantity_2 = record.quantity_2 if record.quantity_2 else 0
            norm = record.detail.parameters_for_spu.norm if record.detail.parameters_for_spu else 0
            price = record.detail.parameters_for_spu.price if record.detail.parameters_for_spu else 0
            price_1 = record.detail.parameters_for_spu.return_salary_per_first_side() if record.detail.parameters_for_spu else 0
            price_2 = record.detail.parameters_for_spu.return_salary_per_second_side() if record.detail.parameters_for_spu else 0
            if (record.product, record.detail) not in dict:
                dict[(record.product, record.detail)] = {
                    'quantity': quantity,
                    'quantity_1': quantity_1,
                    'quantity_2': quantity_2,
                    'norm': norm,
                    'price': price,
                    'price_1': price_1,
                    'price_2': price_2,
                    'order_yes': 1 if record.order_yes else 0,
                    'order_at_master': 1 if record.order_at_master else 0
                }
            else:
                dict[(record.product, record.detail)]['quantity'] += record.quantity if record.quantity else 0
                dict[(record.product, record.detail)]['quantity_1'] += record.quantity_1 if record.quantity_1 else 0
                dict[(record.product, record.detail)]['quantity_2'] += record.quantity_2 if record.quantity_2 else 0
                dict[(record.product, record.detail)]['order_yes'] += record.order_yes
                dict[(record.product, record.detail)]['order_at_master'] += record.order_at_master
            dict[(record.product, record.detail)]['salary'] = round(((dict[(record.product, record.detail)]['quantity'] *  dict[(record.product, record.detail)]['price'] +\
                                     dict[(record.product, record.detail)]['quantity_1'] * dict[(record.product, record.detail)]['price_1'] +\
                                     dict[(record.product, record.detail)]['quantity_2'] * dict[(record.product, record.detail)]['price_2']) * 1.4), 2)
        return dict
    except AttributeError:
        return HttpResponse("Exception: Data not found")


def get_records_for_str_name(record, worker, month):
    """Ищет все записи модели RecordJob по строковому названию. Возвращает queryset с RecordJob"""
    from workshop_data.models import RecordJob, Product, Detail
    if isinstance(record, str):
        product = record.split(',')[0].split(' ')[1][:-1]
        detail = record.split(',')[1].split(' ')[2].split('.')[1][:-2]
        records = RecordJob.objects.filter(user=worker,
                                           month=month,
                                           product=Product.objects.get(name=product),
                                           detail=Detail.objects.get(name=detail))
    else:
        records = RecordJob.objects.filter(user=worker,
                                           month=month,
                                           product=record[0],
                                           detail=record[1])
    return records


def record_job_order_yes_ready(request, worker, month, record):
    records = get_records_for_str_name(record, worker, month)
    records.update(order_yes=True) if records[0].order_yes == False else records.update(order_yes=False)
    return HttpResponseRedirect(reverse_lazy(
        'all_record_job_for_worker_per_month',
        kwargs={'id': records[0].user.id, 'month': records[0].month}))


def record_job_order_at_master(request, worker, month, record):
    """Меняет значение поля order_at_master модели RecordJob"""
    records = get_records_for_str_name(record, worker, month)
    records.update(order_at_master=True) if records[0].order_at_master == False else records.update(order_at_master=False)
    return HttpResponseRedirect(reverse_lazy(
        'all_record_job_for_worker_per_month',
        kwargs={'id': records[0].user.id, 'month': records[0].month}))


def return_quantity_for_order(worker, month, record):
    """Возвращает количество деталей из списка записей RecordJob(для заполнения наряда)"""
    records = get_records_for_str_name(record, worker, month)
    count = 0
    for record in records:
        count += record.quantity
        count += record.quantity_1 / 2
        count += record.quantity_2 / 2
    return int(count)


def counter_norm(month, worker):
    """Считает норму времени сделанных деталей"""
    from workshop_data.models import RecordJob
    records = RecordJob.objects.filter(user=worker, month=month)
    norm_time = 0

    for key, value, in return_sum_recordjob_every_detail(records).items():
        print()
        print(value)
        print()
        norm_time += value['quantity'] * value['norm'] +\
                     value['quantity_1'] / 2 * value['norm'] \
                     + value['quantity_2'] / 2 * value['norm']
    return round(norm_time, 2)


def return_detail_by_product_detail(record):
    """Возвращает деталь по названию детали и префиксу"""
    from workshop_data.models import Product, Detail, Prefix
    # product = Product.objects.get(name=record.split()[0])
    detail = record.split()[1]
    if len(detail.split('.')) > 1:
        name = detail.split('.')[1]
        prefix = Prefix.objects.get(name=detail.split('.')[0])
        object = Detail.objects.get(name=name, prefix=prefix)
    else:
        object = Detail.objects.get(detail=detail)
    return object


def return_product_that_the_detail_is_included(detail):
    """Находит изделие в который входит деталь"""
    if detail.detail_in_detail.first().detail_in_detail.first().detail_in_detail.exists():
        return detail.detail_in_detail.first().detail_in_detail.first().detail_in_detail.first().detail_in_product.first()
    elif detail.detail_in_detail.first().detail_in_detail.exists():
        return detail.detail_in_detail.first().detail_in_detail.first().detail_in_product.first()
    elif detail.detail_in_detail.exists():
        return detail.detail_in_detail.first().detail_in_product.first()
    else:
        return detail.detail_in_product.first()
