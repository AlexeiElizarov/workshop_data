from django import forms
from django.shortcuts import render
from django.views.generic import UpdateView

from workshop_data.models.order import Order
from workshop_data.models.stage_manufacturing_detail_in_work import StageManufacturingDetailInWork
from django.http import JsonResponse

def test_form(request):
    form = TestForm()
    if request.method == "POST" and request.accepts('text/html'):
        form = TestForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            time_of_work = form.cleaned_data['time_of_work']
            # form.save()
            return JsonResponse({"time_of_work": time_of_work}, status=200)
        else:
            errors = form.errors.as_json()
            return JsonResponse({"errors": errors}, status=400)

    return render(request, "workshop_data/worker/order/order_main_template.html", {"form": form})




class TestForm(forms.ModelForm):
    class Meta:
        model = StageManufacturingDetailInWork
        # fields = ('time_of_work',)
        fields = '__all__'


class TestView(UpdateView):
    template_name = 'workshop_data/worker/order/test.html'
    form_class = TestForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('id')
        return Order.objects.get(pk=46)


# <button type="button" class="btn btn-primary"
#                             style="--bs-btn-padding-y: .1rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .8rem;">
#                         Ввести
#                     </button>
#


# <input class="btn btn-primary" type="text">
#                     <button type="button" class="btn btn-primary"
#                             style="--bs-btn-padding-y: .1rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .8rem;">
#                         Ввести
#                     </button>