from dal import autocomplete

from ..models import *
from sign.models import User, LIST_POSITION_WORKER


class WorkerAutocomplete(autocomplete.Select2QuerySetView):
    """Реализует поле авто подсказки Рабочего по вводимым символам"""
    def get_result_label(self, result):
        """Меняет __str__() представление модели на get_full_name()"""
        return result.get_full_name()

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return User.objects.none()
        qs = User.objects.filter(position__in=LIST_POSITION_WORKER)
        if self.q:
            qs = qs.filter(surname__istartswith=self.q)
        return qs


class ProductAutocomplete(autocomplete.Select2QuerySetView):
    """Реализует поле авто подсказки Изделий по вводимым символам"""

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Product.objects.none()
        qs = Product.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class DetailAutocomplete(autocomplete.Select2QuerySetView):
    """Реализует поле авто подсказки Деталей по вводимым символам"""

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Detail.objects.none()
        qs = Detail.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


# class NodeAutocomplete(autocomplete.Select2QuerySetView):
#     """Реализует поле авто подсказки Деталей по вводимым символам"""
#
#     def get_queryset(self):
#         if not self.request.user.is_authenticated:
#             return Detail.objects.none()
#         qs = Node.objects.all()
#         if self.q:
#             qs = qs.filter(name__istartswith=self.q)
#         return qs


# class NodeAndDetailAutocomplete(autocomplete.Select2QuerySetView):
#     """Реализует поле авто подсказки Деталей по вводимым символам"""
#
#     def get_queryset(self):
#         if not self.request.user.is_authenticated:
#             return Detail.objects.none()
#         qs = Node.objects.all() + Detail.objects.all()
#         if self.q:
#             qs = qs.filter(name__istartswith=self.q)
#         return qs


class CategoryDetailAutocomplete(autocomplete.Select2QuerySetView):
    """Реализует поле авто подсказки Категории Деталей по вводимыи символам"""

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CategoryDetail.objects.none()
        qs = CategoryDetail.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class BatchlAutocomplete(autocomplete.Select2QuerySetView):
    """Реализует поле авто подсказки ID Партии"""

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return BatchDetailInPlan.objects.none()
        qs = BatchDetailInPlan.objects.all()
        if self.q:
            qs = qs.filter(id__istartswith=self.q)
        return qs
