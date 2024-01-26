from django.db.models import Avg, Sum
from django.shortcuts import redirect

from sign.forms import User
from workshop_data.models.record_job import EvaluationOfTheOperatorsWork, ID_OPERATORS


def get_average_coefficient_all_operator():
    """Высчитывает средний коэффициент для всех операторов и обновляет в БД"""
    for id in ID_OPERATORS:
        worker = User.objects.get(id=id)
        # avg_coef = EvaluationOfTheOperatorsWork.objects.filter(worker=worker).aggregate(Avg("coefficient_for_day", default=0))
        from django.db.models.functions import TruncDay
        from django.db.models import Max
        q = EvaluationOfTheOperatorsWork.objects.filter(worker=worker).annotate(
            day=TruncDay('date')
        ).values('coefficient_for_day').annotate(last_id=Max('id')).aggregate(Avg("coefficient_for_day", default=0))
        if q['coefficient_for_day__avg'] is not None:
            worker.average_coefficient_operator = round(q['coefficient_for_day__avg'], 2)
            worker.save()
        else:
            worker.average_coefficient_operator = 0
    return redirect('average_coefficient_operators')


def get_average_coefficient_operator_range_date(date1, date2) -> dict:
    """Вычисляет средний коэффициент операторов в диапазоне дат"""
    avg_coefficient_operator_dict = {}
    for operator_id in ID_OPERATORS:
        worker = User.objects.get(id=operator_id)
        avg = (EvaluationOfTheOperatorsWork.objects.
               filter(worker=worker).filter(date__range=(date1, date2)).
               aggregate(Avg("coefficient_for_day")))
        avg_coefficient_operator_dict[worker.get_full_name()] = [
            round(avg['coefficient_for_day__avg'], 2) if avg['coefficient_for_day__avg'] is not None else 0]
    return avg_coefficient_operator_dict


def update_database_after_deleting_record_work_time(worker, date):
    """Обновляет 'coefficient_for_day' у всех записей за данный день после удаления записи о работе оператора"""
    date = date
    worker = User.objects.get(username=worker)
    coefficient_for_day = round(EvaluationOfTheOperatorsWork.objects.filter(
        worker=worker, date=date).aggregate(Sum("coefficient"))['coefficient__sum'], 2)
    q = EvaluationOfTheOperatorsWork.objects.filter(worker=worker, date=date)
    for record in q:
        record.coefficient_for_day = coefficient_for_day
    EvaluationOfTheOperatorsWork.objects.bulk_update(q, ['coefficient_for_day'])



