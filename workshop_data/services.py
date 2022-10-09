


def replacing_True_False_flag(request):
    print(request.GET)
    print(request.GET.kwargs)
    return HttpResponseRedirect(reverse_lazy('start_new_stage_in_work_complete'))
