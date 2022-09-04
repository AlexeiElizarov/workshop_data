from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

from .views import *
urlpatterns = [
    path('data_autocomplete_product/', ProductAutocomplete.as_view(), name='data_autocomplete_product'),
    path('data_autocomplete_detail/', DetailAutocomplete.as_view(), name='data_autocomplete_detail'),
    path('data_autocomplete_worker/', WorkerAutocomplete.as_view(create_field='name'), name='data_autocomplete_worker'),
    path('data_autocomplete_categorydetail/', CategoryDetailAutocomplete.as_view(), name='data_autocomplete_category_detail'),

    path('detail/all/', DetailAllView.as_view(), name='detail_list_all'),
    path('new-detail/', DetailCreateView.as_view(), name='create_new_detail'),
    path('new-detail-complite/', detaile_create_complite, name='create_new_detail_complite'),
    path('add-detail-complite/', product_add_detail_complite, name='product_add_detail_complite'),

    path('<product>/add-detail/', ProductAddDetailView.as_view(), name='product_add_detail'),
    path('<product>/detail/', ProductDataView.as_view(), name='product_detail_data'),
    path('product/all/', ProductAllView.as_view(), name='product_list_all'),
    path('new-product/', ProductCreateView.as_view(), name='create_new_product'),
    path('new-product-complite/', product_create_complite, name='create_new_product_complite'),

    path('<username>/create_new_order/', OrderUserCreateView.as_view(), name='order_user_create'),
    path('<username>/all_orders/', OrderUserParametrListView.as_view(), name='orders_user_list_all'),
    path('<username>/<id>/edit/', OrderUserEditView.as_view(), name='order_user_edit'),
    path('<username>/<id>/delete/', OrderDeleteView.as_view(), name='order_user_delete'),
    path('<username>/month_<str:month>/', OrderUserParametrListView.as_view(), name='orders_user_month_list'),
    path('<username>/product_<str:product>/', OrderUserParametrListView.as_view(), name='orders_user_product_list'),
    path('<username>/detail_<str:detail>/', OrderUserParametrListView.as_view(), name='orders_user_detail_list'),
    path('<username>/category_<str:category>/', OrderUserParametrListView.as_view(), name='orders_user_detailcategory_list'),

    path('master/workers-all-list/', WorkerListView.as_view(), name='workers_list_all'),
    path('master/workers-LSM-list/', WorkerListView.as_view(), {'LSM': True},  name='workers_LSM_all'),
    path('master/workers-TRN-list/', WorkerListView.as_view(), {'TRN': True},  name='workers_TRN_all'),
    path('master/orders-<surname>-<name>/', WorkerOrdersListForMaster.as_view(), name='orders-worker-for-master'),
    path('master/orders-<surname>-<name>/month_<month>/', WorkerOrdersListForMaster.as_view(), name='orders-worker-month-for-master'),

    path('plan/product-add-in-plan-complite/', product_add_in_plan_complite, name='product_add_plan_complite'),
    path('plan/product-add-in-plan/', WorkshopPlanCreateView.as_view(), name='product_add_plan'),
    path('plan/<year>-<month>/', WorkshopPlanView.as_view(), name='plan'),
]
