from django.shortcuts import render

def product_create_complite(request):
    return render(request, 'workshop_data/worker/product_create_complite.html')


def detaile_create_complite(request):
    return render(request, 'workshop_data/detail/detail_create_complite.html')


def product_add_detail_complite(request):
    return render(request, 'workshop_data/product/product_add_detail_complite.html')


def product_add_in_plan_complite(request):
    return render(request, 'workshop_data/plan/product_add_in_plan.html')


def add_stage_in_detail_complite(request):
    return render(request, 'workshop_data/detail/stage/add_stage_in_detail_complite.html')


def new_batch_complite(request):
    return render(request, 'workshop_data/master/batch/new_batch_create_complite.html')


def start_new_stage_in_work_complite(request):
    return render(request, 'workshop_data/master/stage_in_work/start_new_stage_in_work_complete.html')

def batch_ready_comlite(request, year, month, id):
    return render(request, 'workshop_data/master/batch/batch_ready_complite.html')