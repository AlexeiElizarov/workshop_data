from django.urls import path
from workshop_data.services.services import stage_in_work_ready
from workshop_data.views.test_views import index, OrderBlankView

from workshop_data.views.services_view import (
    ProductAutocomplete,
    DetailAutocomplete,
    WorkerAutocomplete,
    CategoryDetailAutocomplete,
    BatchlAutocomplete)
from workshop_data.views.stage_views import (
    StageManufacturingDetailInWorkInPlanView,
    StageManufacturingDetailInWorkView,
    EditStageManufacturingDetailInWorkView,
    EditStageInDetailView,
    StageInDetailView,
    AddStageInDeatailVeiw)
from workshop_data.views.complite_view import *
from workshop_data.views.detail_view import (
    DetailAllView,
    DetailCreateView)
from workshop_data.views.product_view import (
    ProductAllView,
    ProductCreateView,
    ProductAddDetailView,
    ProductDataView)
from workshop_data.views.order_views import (
    OrderUserCreateView,
    OrderUserParametrListView,
    OrderUserEditView,
    OrderDeleteView, TimeOfWorkInStage)
from workshop_data.views.master_views import (
    WorkerOrdersListForMaster,
    WorkerListView, WorkerAveragePriceListForMaster)
from workshop_data.views.batch_views import (
    CreateBatchDetailInPlan,
    AllBatchDetailInPlanView,
    DeleteBatchDetailInPlanView,
    AllBatchDetailProductInPlan)
from workshop_data.views.workshopplan_views import (
    WorkshopPlanUpdateView,
    WorkshopPlanDeleteView,
    WorkshopPlanCreateView,
    WorkshopPlanView)
from workshop_data.services.services import batch_ready, batch_cancel_ready

urlpatterns = [
    path('data_autocomplete_product/', ProductAutocomplete.as_view(), name='data_autocomplete_product'),
    path('data_autocomplete_detail/', DetailAutocomplete.as_view(), name='data_autocomplete_detail'),
    path('data_autocomplete_worker/', WorkerAutocomplete.as_view(create_field='name'), name='data_autocomplete_worker'),
    path('data_autocomplete_categorydetail/', CategoryDetailAutocomplete.as_view(), name='data_autocomplete_category_detail'),
    path('data_autocomplete_batch/', BatchlAutocomplete.as_view(), name='data_autocomplete_batch'),

    path('<pk>/edit-stage-in-detail', EditStageInDetailView.as_view(), name='edit_stage_in_detail'),
    path('<pk>/all-stage-in-detail', StageInDetailView.as_view(), name='all_stage_in_detail'),
    path('<pk>/add-stage-in-detail/', AddStageInDeatailVeiw.as_view(), name='add_stage_in_detail'),
    path('add-stage-in-detail-complite/', add_stage_in_detail_complite, name='add_stage_in_detail_complite'),
    path('new-detail-complite/', detaile_create_complite, name='create_new_detail_complite'),
    path('add-detail-complite/', product_add_detail_complite, name='product_add_detail_complite'),
    path('new-detail/', DetailCreateView.as_view(), name='create_new_detail'),
    path('detail/all/', DetailAllView.as_view(), name='detail_list_all'),

    path('<product>/add-detail/', ProductAddDetailView.as_view(), name='product_add_detail'),
    path('<product>/detail/', ProductDataView.as_view(), name='product_detail_data'),
    path('product/all/', ProductAllView.as_view(), name='product_list_all'),
    path('new-product/', ProductCreateView.as_view(), name='create_new_product'),
    path('new-product-complite/', product_create_complite, name='create_new_product_complite'),

    path('<username>/create_new_order/', OrderUserCreateView.as_view(), name='order_user_create'),
    path('<username>/all_orders/batch-<batch>/operations-<operations>', stage_in_work_ready, name='stage_work_done'),
    path('<username>/all_orders/', OrderUserParametrListView.as_view(), name='orders_user_list_all'),
    path('<username>/<id>/edit/', OrderUserEditView.as_view(), name='order_user_edit'),
    path('<username>/<id>/delete/', OrderDeleteView.as_view(), name='order_user_delete'),
    path('<username>/month_<str:month>/', OrderUserParametrListView.as_view(), name='orders_user_month_list'),

    path('master/workers-all-list/', WorkerListView.as_view(), name='workers_list_all'),
    path('master/workers-LSM-list/', WorkerListView.as_view(), {'LSM': True},  name='workers_LSM_all'),
    path('master/workers-TRN-list/', WorkerListView.as_view(), {'TRN': True},  name='workers_TRN_all'),
    path('master/orders-<surname>-<name>/', OrderUserParametrListView.as_view(), name='orders-worker-for-master'),
    path('master/orders-<surname>-<name>/month_<month>/', OrderUserParametrListView.as_view(), name='orders-worker-month-for-master'),
    path('master/orders-<surname>-<name>/product_<str:product>/', OrderUserParametrListView.as_view(), name='orders_user_product_list'),
    path('master/orders-<surname>-<name>/detail_<str:detail>/', OrderUserParametrListView.as_view(), name='orders_user_detail_list'),
    path('master/orders-<surname>-<name>/category_<str:category>/', OrderUserParametrListView.as_view(), name='orders_user_detailcategory_list'),
    path('master/workers-average-price/', WorkerAveragePriceListForMaster.as_view(), name='master_workers_average_price_list'),


    path('master/all-batch-in-plan/', AllBatchDetailInPlanView.as_view(), name='all_batch_in_plan'),
    path('master/create-new-batch/<product>/', CreateBatchDetailInPlan.as_view(), name='create_new_batch'),
    path('master/create-new-batch/complite/', new_batch_complite, name='new_batch_complite'),
    path('master/start-new-stage-in-work/batch-<batch>/edit/', EditStageManufacturingDetailInWorkView.as_view(), name='edit_start_new_stage_in_work'),
    path('master/start-new-stage-in-work/batch-<batch>/', StageManufacturingDetailInWorkView.as_view(), name='start_new_stage_in_work'),
    path('master/start-new-stage-in-work/complite/', start_new_stage_in_work_complite, name='start_new_stage_in_work_complete'),
    path('master/all-stage-in-work/batch-<id>', StageManufacturingDetailInWorkInPlanView.as_view(), name='all_stage_this_batch'),
    path('master/batchs-in-plan/<object>/', AllBatchDetailProductInPlan.as_view(), name='batchs_in_plan'),
    path('master/delete-batch/<id>', DeleteBatchDetailInPlanView.as_view(), name='delete_batch'),


    path('plan/product-add-in-plan-complite/', product_add_in_plan_complite, name='product_add_plan_complite'),
    path('plan/product-add-in-plan/', WorkshopPlanCreateView.as_view(), name='product_add_plan'),
    path('plan/<year>-<month>/', WorkshopPlanView.as_view(), name='plan'),
    path('plan/<year>-<month>/delete-<object>/', WorkshopPlanDeleteView.as_view(), name='delete_object_from_workshopplan'),
    path('plan/<year>-<month>/update-<object>/', WorkshopPlanUpdateView.as_view(), name='update_object_from_workshopplan'),

    path('plan/<year>-<month>/batch-<id>/ready/', batch_ready, name='batch_ready_in_plan'),
    path('plan/<year>-<month>/batch-<id>/ready_cancel/', batch_cancel_ready, name='batch_cancel_ready_in_plan'),
    path('plan/<year>-<month>/batch-<id>/ready_complite/', batch_ready_comlite, name='batch_ready_comlite'),

    path('test_view/', OrderBlankView.as_view(), name='test_order_form'),
    path('testform/', index, name='testform'),
    path('test_view/<username>/<id>/', TimeOfWorkInStage.as_view(), name='order_user_edit_test')

]


