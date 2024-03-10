from django import template

from workshop_data.models import WorkshopPlan, Product, Detail
from workshop_data.services import current_year
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()


@register.simple_tag(name='object_workshopplan')
def get_workshopplan_object_for_month_tag(product: Product, detail: Detail, month):
    """Возвращает """
    try:
        return WorkshopPlan.objects.select_related('product', 'detail', 'detail__prefix',).\
            get(product=product, detail=detail, month__in=month)
    except ObjectDoesNotExist:
        # запросу не соответствует ни один элемент.
        pass
    except WorkshopPlan.MultipleObjectsReturned:
        # запросу соответствует несколько элементов.
        pass


# @register.simple_tag(name='remove_object_workshopplan')
# def remove_workshopplan_object_tag(queryset, obj):
#     """Удаляет элемент из набора запросов"""
#     queryset.exclude(id=obj.id)
#     return queryset




@register.simple_tag(name='intersection_query_sets')
def get_workshopplan_object_for_month_tag(detail: Detail, month):
    workshopplan_details = Detail.objects.none()
    for object in WorkshopPlan.objects.filter(month=month):
        workshopplan_details |= object.detail
    if detail.secondary_detail.all() & workshopplan_details:
        return True


# @register.simple_tag(name='quantity')
# def get_workshopplan_object_quantity_for_month_tag(detail: Detail, month):
#     """Возвращает """
#     if month:
#         try:
#             return WorkshopPlan.objects.get(
#                 detail=detail,
#                 month__in=month,
#                 year=current_year()).get_quantity()
#         except:
#             return '--'
#     elif month == None:
#         return


# @register.simple_tag(name='quantity_state_order')
# def get_workshopplan_object_quantity_state_order_for_month_tag(detail: Detail, month):
#     """Возвращает """
#     if month:
#         try:
#             return WorkshopPlan.objects.get(
#                 detail=detail,
#                 month__in=month,
#                 year=current_year()).quantity_state_order
#         except:
#             return '--'
#     elif month == None:
#         return


# @register.simple_tag(name='quantity_commercial_order')
# def get_workshopplan_object_quantity_commercial_order_state_order_for_month_tag(detail: Detail, month):
#     """Возвращает """
#     if month:
#         try:
#             return WorkshopPlan.objects.get(
#                 detail=detail,
#                 month__in=month,
#                 year=current_year()).select_related('detail').quantity_commercial_order
#         except:
#             return '--'
#     elif month == None:
#         return
