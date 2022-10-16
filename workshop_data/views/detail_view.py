from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from ..models import Detail
from ..filters import DetailFilter
from ..forms import DetailCreateForm


class DetailAllView(ListView):
    '''Отображает страницу со всеми Деталями'''
    model = Detail
    template_name = 'workshop_data/detail/detail_list_all.html'
    context_object_name = 'details'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['filter'] = DetailFilter(self.request.GET, queryset=self.get_queryset())
        return context


class DetailCreateView(CreateView):
    '''Отображает страницу создания новоой Детали'''
    model = Detail
    form_class = DetailCreateForm
    template_name = 'workshop_data/detail/detail_create.html'
    success_url = reverse_lazy('create_new_detail_complite')