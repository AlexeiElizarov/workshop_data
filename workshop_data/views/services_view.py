from dal import autocomplete

from ..models import *
from sign.models import User

def sum_parametrs(list_objects):
    '''Считает сумму зарплаты списка нарядов '''
    lst = []
    for obj in list_objects:
        salary = float(obj.price) * int(obj.quantity) * 1.4
        lst.append(salary)
    return sum(lst)

class WorkerAutocomplete(autocomplete.Select2QuerySetView):
    '''Реализует поле автоподсказки Рабочего по вводимыи символам'''

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return User.objects.none()
        qs = User.objects.all()
        if self.q:
            qs = qs.filter(surname__istartswith=self.q)
        return qs


class ProductAutocomplete(autocomplete.Select2QuerySetView):
    '''Реализует поле автоподсказки Изделий по вводимыи символам'''

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Product.objects.none()
        qs = Product.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class DetailAutocomplete(autocomplete.Select2QuerySetView):
    '''Реализует поле автоподсказки Деталей по вводимыи символам'''

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Detail.objects.none()
        qs = Detail.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class CategoryDetailAutocomplete(autocomplete.Select2QuerySetView):
    '''Реализует поле автоподсказки Категории Деталей по вводимыи символам'''

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CategoryDetail.objects.none()
        qs = CategoryDetail.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs