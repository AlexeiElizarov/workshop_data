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



class StageForDetaillAutocomplete(autocomplete.Select2QuerySetView):
    """Реализует поле авто подсказки этапов производства в зависимости от выбранной детали"""

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return StageManufacturingDetail.objects.none()
        qs = StageManufacturingDetail.objects.all()
        detail = self.forwarded.get('detail', None)
        if detail:
            qs = qs.filter(detail=detail)
        if self.q:
            qs = qs.filter(operations__istartswith=self.q)
        return qs


class DetaillForProductAutocomplete(autocomplete.Select2QuerySetView):
    """Реализует поле авто подсказки деталей в зависимости от выбранного изделия"""

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Detail.objects.none()
        qs = Detail.objects.all()
        product = self.forwarded.get('product', None)
        if product:
            qs = qs.filter(detail_in_product=product)
            for detail in qs:
                qs = qs.union(detail.secondary_detail.all())
                for detail in detail.secondary_detail.all():
                    qs = qs.union(detail.secondary_detail.all())
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs