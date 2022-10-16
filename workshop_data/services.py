from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import BatchDetailInPlan


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

