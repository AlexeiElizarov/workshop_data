from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from workshop_data.models import Order


class ShiftTask(LoginRequiredMixin, ListView):
    """Отображает страницу сменного задания"""
    model = Order
    template_name = 'workshop_data/master/any_template/shift_task_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['orders'] = Order.objects.all()
        return context
