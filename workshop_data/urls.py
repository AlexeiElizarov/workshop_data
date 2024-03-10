from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from workshop_data.services.general_services import (
    stage_in_work_ready,
    resolution_statement_about_job_over_detail, record_job_order_yes_ready, record_job_order_at_master)
from workshop_data.views.statement_about_job_over_detail_view import (
    AllDetailResolutionOrNotView,
    StatementAboutJobOverDetailView,)
from workshop_data.views import (
    CreateNewBonusView,
    ListAllBonuses,
    ListAllWorkersAndBonuses,
    UpdateBonusView)
from workshop_data.views.services_view import (
    ProductAutocomplete,
    DetailAutocomplete,
    WorkerAutocomplete,
    CategoryDetailAutocomplete,
    BatchlAutocomplete,
    StageForDetaillAutocomplete,
    DetaillForProductAutocomplete,
    WorkerSPUAutocomplete,
)
from workshop_data.views.stage_views import (
    StageManufacturingDetailInWorkInPlanView,
    StageManufacturingDetailInWorkView,
    EditStageManufacturingDetailInWorkView,
    EditStageInDetailView,
    StageInDetailView,
    AddStageInDeatailVeiw,
    EnteringDetailToViewAverageTimeOfWorkView)
from workshop_data.views.complite_view import *
from workshop_data.views.detail_view import (
    DetailAllView,
    DetailCreateView,
    DetailDeleteView,
    AddImageInDetailView,
    DetailImageView,
    DetailAddDetailView,
    DetailEditView,)
from workshop_data.views.product_view import (
    ProductAllView,
    ProductCreateView,
    ProductAddDetailView,
    ProductDataView,
    ProductDeleteView,
    DeleteDetailFromProductView,)
from workshop_data.views.order_views import (
    OrderUserCreateView,
    OrderUserParametrListView,
    OrderUserEditView,
    OrderDeleteView,
    TimeOfWorkInStage,
    AllOrderForAllWorker,
    OrderUserEditMonthView,
)
from workshop_data.views.master_views import (
    # WorkerOrdersListForMaster,
    WorkerListView,
    WorkerAveragePriceListForMaster,
    WorkerSalaryListView)
from workshop_data.views.batch_views import (
    CreateBatchDetailInPlan,
    AllBatchDetailInPlanView,
    # DeleteBatchDetailInPlanView,
    AllBatchDetailProductInPlan)
from workshop_data.views.warehouse_view import (
    WarehouseCreateView,
    WarehouseUpdateView,
    WarehouseListView,
    ViewWarehouseRecord,
    WarehouseCreateSelectedDetailView, WarehouseDeleteView,
)
from workshop_data.views.workshopplan_views import (
    WorkshopPlanUpdateView,
    WorkshopPlanDeleteView,
    WorkshopPlanCreateView,
    WorkshopPlanView,
    WorkshopPlanAddExistingBatchView)
from workshop_data.views.category_detail_views import (
    CreateCategoryDetailView,
    CategoryDetailAllList,
    CategoryDetailUpdateView, CategoryDetailDeleteView,
)
from workshop_data.views.any_view import ShiftTask
from workshop_data.services.general_services import batch_ready, batch_cancel_ready
from workshop_data.views.comment_view import (
    CommentUpdateView,
    WorkshopPlanCommentCreateView,
)
from workshop_data.views.record_job_view import (
    RecordJobCreateView,
    RecordJobEditView,
    AllRecordJobForAllWorker,
    DiagramWorkSPUView,
    ParametersDetailForSPUCreateView,
    ParametersDetailForSPEditeView,
    parameters_detail_for_spu_create_or_edit_redirect,
    RecordJobDeleteView,
    AllRecordJobForWorker,
    AllRecordJobForWorkerPerMonth,
    MillingDetailForSPUCreateView,
    EnteringOperatorWorkTimeView,
    AllOperatorWorkTimeView,
    AverageCoefficientOperators,
    DeletingOperatorWorkTimeView,
    EditOperatorWorkTimeView,
    DiagramWorkTimeOperatorView,
)
from workshop_data.services.evaluation_work_time import get_average_coefficient_all_operator


urlpatterns = [
    path('data_autocomplete_product/', ProductAutocomplete.as_view(), name='data_autocomplete_product'),
    path('data_autocomplete_detail/', DetailAutocomplete.as_view(), name='data_autocomplete_detail'),
    path('data_autocomplete_worker/', WorkerAutocomplete.as_view(), name='data_autocomplete_worker'),
    path('data_autocomplete_worker_spu/', WorkerSPUAutocomplete.as_view(), name='data_autocomplete_worker_cpu'),
    path('data_autocomplete_categorydetail/', CategoryDetailAutocomplete.as_view(), name='data_autocomplete_category_detail'),
    path('data_autocomplete_batch/', BatchlAutocomplete.as_view(), name='data_autocomplete_batch'),
    path('data_autocomplete_satage_in_detail/', StageForDetaillAutocomplete.as_view(), name='data_autocomplete_stage_in_detail'),
    path('data_autocomplete_detail_for_product/', DetaillForProductAutocomplete.as_view(), name='data_autocomplete_detail_for_product'),

    path('<pk>/edit-stage-in-detail/', EditStageInDetailView.as_view(), name='edit_stage_in_detail'),
    path('<pk>/<detail>/all-stage-in-detail/', StageInDetailView.as_view(), name='all_stage_in_detail'),
    path('<pk>/<node>/all-stage-in-node/', StageInDetailView.as_view(), name='all_stage_in_node'),
    path('detail-<detail_id>/add-stage-in-detail/', AddStageInDeatailVeiw.as_view(), name='add_stage_in_detail'),
    path('node-<node_id>/add-stage-in-node/', AddStageInDeatailVeiw.as_view(), name='add_stage_in_node'),
    path('add-stage-in-detail-complete/', add_stage_in_detail_complite, name='add_stage_in_detail_complete'),
    path('new-detail-complete/', detaile_create_complite, name='create_new_detail_complete'),
    path('add-detail-complete/', product_add_detail_complite, name='product_add_detail_complete'),
    path('<detail>/add-detail-in-detail/', DetailAddDetailView.as_view(), name='detail_add_detail'),

    path('new-detail/', DetailCreateView.as_view(), name='create_new_detail'),
    path('edit-detail/<name>/', DetailEditView.as_view(), name='edit_detail'),
    path('detail/all/', DetailAllView.as_view(), name='detail_list_all'),
    path('detail-delete/<id>/', DetailDeleteView.as_view(), name='detail_delete'),
    path('add-image-in-<detail>/', AddImageInDetailView.as_view(), name='add_image_in_detail'),
    path('image-<pk>/', DetailImageView.as_view(), name='image_detail'),

    path('<product>/add-detail/', ProductAddDetailView.as_view(), name='product_add_detail'),
    path('<str:slug>/detail/', ProductDataView.as_view(), name='product_detail_data'),
    path('<product>/delete-<detail>/',DeleteDetailFromProductView.as_view(), name='delete_detail_from_product'),
    path('product/all/', ProductAllView.as_view(), name='product_list_all'),
    path('new-product/', ProductCreateView.as_view(), name='create_new_product'),
    path('new-product-complete/', product_create_complite, name='create_new_product_complete'),
    path('delete-product/<product_name>/', ProductDeleteView.as_view(), name='product_delete'),

    path('create-new-category/', CreateCategoryDetailView.as_view(), name='create_new_category'),
    path('category_detail_all_list/', CategoryDetailAllList.as_view(), name='category_detail_all_list'),
    path('category_detail_update/<id>/', CategoryDetailUpdateView.as_view(), name='category_detail_update'),
    path('category_detail_delete/<id>/', CategoryDetailDeleteView.as_view(), name='category_detail_delete'),
    path('category_detail_list/<str:category>/', DetailAllView.as_view(), name='category_detail_list_all'),

    path('<username>/create_new_order/', OrderUserCreateView.as_view(), name='order_user_create'),
    path('<username>/all_orders/batch-<batch>/operations-<operations>', stage_in_work_ready, name='stage_work_done'),
    path('all_orders/', AllOrderForAllWorker.as_view(), name='all_orders_list_for_all_workers'),
    path('master/all_orders/month_<month>/', AllOrderForAllWorker.as_view(), name='all_orders_list_for_all_workers_month'),
    path('master/all_orders/orders-<username>/', AllOrderForAllWorker.as_view(), name='orders-worker-surname-for-master'),
    path('master/all_orders/product_<str:product>/', AllOrderForAllWorker.as_view(), name='all_orders_list_for_all_workers_product'),
    path('master/all_orders/detail_<str:detail_id>/', AllOrderForAllWorker.as_view(), name='all_orders_list_for_all_workers_detail'),
    path('master/all_orders/category_<str:category>/', AllOrderForAllWorker.as_view(), name='all_orders_list_for_all_workers_category'),
    path('<username>/all_orders/', OrderUserParametrListView.as_view(), name='orders_user_list_all'),
    path('<username>/<id>/edit/', OrderUserEditView.as_view(), name='order_user_edit'),
    path('<username>/<id>/delete/', OrderDeleteView.as_view(), name='order_user_delete'),
    path('<username>/month_<str:month>/', OrderUserParametrListView.as_view(), name='orders_user_month_list'),
    path('<username>/statement_about_job_over_detail/', StatementAboutJobOverDetailView.as_view(), name='statement_for_detail'),
    path('<username>/list_all_resolution_or_not_detail/', AllDetailResolutionOrNotView.as_view(), name='list_all_resolution_or_not_detail'),
    path('<username>/resolution_or_not_detail/<id>/done/', resolution_statement_about_job_over_detail, name='resolution_statement_done'),
    path('<username>/order_<id>_edit_month/', OrderUserEditMonthView.as_view(), name='order_user_edit_month'),

    path('master/workers-all-list/', WorkerListView.as_view(), name='workers_list_all'),
    path('master/workers-<position>-list/', WorkerListView.as_view(), name='workers_list_position'),
    path('master/workers-LSM-list/', WorkerListView.as_view(), {'LSM': True},  name='workers_LSM_all'),
    path('master/workers-TRN-list/', WorkerListView.as_view(), {'TRN': True},  name='workers_TRN_all'),
    path('master/workers-MLR-list/', WorkerListView.as_view(), {'MLR': True},  name='workers_MLR_all'),
    path('master/workers-salary-list/', WorkerSalaryListView.as_view(),  name='workers_salary_all'),
    path('master/orders-<username>/', OrderUserParametrListView.as_view(), name='orders-worker-for-master'),
    path('master/orders-<username>/month_<month>/', OrderUserParametrListView.as_view(), name='orders-worker-month-for-master'),
    path('master/orders-<username>/product_<str:product>/', OrderUserParametrListView.as_view(), name='orders_user_product_list'),
    path('master/orders-<username>/detail_<str:detail>/', OrderUserParametrListView.as_view(), name='orders_user_detail_list'),
    path('master/orders-<username>/category_<str:category>/', OrderUserParametrListView.as_view(), name='orders_user_detailcategory_list'),
    path('master/workers-average-price/', WorkerAveragePriceListForMaster.as_view(), name='master_workers_average_price_list'),
    # path('master/template-order-for-print/', ViewingTemplateOrderView.as_view(), name='viewing-template-order-for-print'),

    path('master/all-batch-in-plan/', AllBatchDetailInPlanView.as_view(), name='all_batch_in_plan'),
    path('master/create-new-batch/<object>/', CreateBatchDetailInPlan.as_view(), name='create_new_batch'),
    path('master/create-new-batch/complete/', new_batch_complite, name='new_batch_complete'),
    path('master/start-new-stage-in-work/batch-<batch>/edit/', EditStageManufacturingDetailInWorkView.as_view(), name='edit_start_new_stage_in_work'),
    path('master/start-new-stage-in-work/batch-<batch>/', StageManufacturingDetailInWorkView.as_view(), name='start_new_stage_in_work'),
    path('master/start-new-stage-in-work/complete/', start_new_stage_in_work_complite, name='start_new_stage_in_work_complete'),
    path('master/all-stage-in-work/batch-<id>', StageManufacturingDetailInWorkInPlanView.as_view(), name='all_stage_this_batch'),
    path('master/average_time_of_work_stage_in_detail/<detail>/<quantity_detail>', EnteringDetailToViewAverageTimeOfWorkView.as_view(), name='average_time_of_work_stage_in_detail_2_parameter'),
    path('master/average_time_of_work_stage_in_detail/<detail>', EnteringDetailToViewAverageTimeOfWorkView.as_view(), name='average_time_of_work_stage_in_detail_1_parameter'),
    path('master/average_time_of_work_stage_in_detail/', EnteringDetailToViewAverageTimeOfWorkView.as_view(), name='average_time_of_work_stage_in_detail' ),
    path('master/batchs-in-plan/<object>/', AllBatchDetailProductInPlan.as_view(), name='batchs_in_plan'),
    # path('master/delete-batch/<id>', DeleteBatchDetailInPlanView.as_view(), name='delete_batch'),


    path('master/task_list/', ShiftTask.as_view(), name='task_list'),
    path('master/commentupdate/', CommentUpdateView.as_view(), name='update_comment'),
    path('master/new-comment-create/plan-<object>/<month>/', WorkshopPlanCommentCreateView.as_view(), name='create_new_comment_workshop_plan'),

    path('master/create-new-bonus/', CreateNewBonusView.as_view(), name='create_new_bonus'),
    path('master/create-bonus-complete/', create_bonus_complete, name='create_bonus_complete'),
    path('master/list-all-bonuses/', ListAllBonuses.as_view(), name='list_bonuses_all_worker'),
    path('master/update-bonus/<id>/',UpdateBonusView.as_view(), name='update-bonus'),
    path('master/list-all-worker-and-here-bonus/', ListAllWorkersAndBonuses.as_view(), name='list_all_worker_here_bonuses'),

    path('evaluation-operator-work/', EnteringOperatorWorkTimeView.as_view(), name='operators_time'),
    path('all-operator-work/', AllOperatorWorkTimeView.as_view(), name='all_operators_time'),
    path('average-coefficient_operators/', AverageCoefficientOperators.as_view(), name='average_coefficient_operators'),
    path('average-all_operators_avg_coef_for_range/', AverageCoefficientOperators.as_view(), name='all_operators_avg_coef_for_range'),
    path('refresh-average-all_operators_avg/', get_average_coefficient_all_operator, name='refresh_all_operators_avg_coef'),
    path('delete-record-operator-work-time/str-<worker>/<date>/<id>/', DeletingOperatorWorkTimeView.as_view(), name='delete_record_operator_work_time'),
    path('edit-record-operator-work-time/str-<worker>/<date>/<id>/', EditOperatorWorkTimeView.as_view(),name='edit_record_operator_work_time'),
    path('diagram-work-time-operator/', DiagramWorkTimeOperatorView.as_view(),name='diagram_work_time_operator'),


    path('record-job-create/', RecordJobCreateView.as_view(),name='record_job_create'),
    path('record-job-edit/<id>/', RecordJobEditView.as_view(),name='record_job_edit'),
    path('record-job-delete/<id>/', RecordJobDeleteView.as_view(),name='record_job_delete'),
    path('record_job/order_at_master/<worker>/<month>/<record>/', record_job_order_at_master,name='record_job_order_at_master'),
    path('record_job/order_yes_ready/<worker>/<month>/<record>/', record_job_order_yes_ready, name='record_job_order_yes_ready'),
    path('all-record-job/', AllRecordJobForAllWorker.as_view(), name='all_record_job'),
    path('all-record-job/worker-<id>/', AllRecordJobForWorker.as_view(), name='all_record_job_for_worker'),
    path('all-record-job/worker-<id>/month-<month>/', AllRecordJobForWorkerPerMonth.as_view(), name='all_record_job_for_worker_per_month'),
    path('all-record-job/mon_<month>/', AllRecordJobForAllWorker.as_view(), name='all_record_job_per_month'),
    path('all-record-job/product_<product>/', AllRecordJobForAllWorker.as_view(), name='all_record_job_per_product'),
    path('all-record-job/detail_<detail>/', AllRecordJobForAllWorker.as_view(), name='all_record_job_per_detail'),
    path('all-record-job/username_<username>/', AllRecordJobForAllWorker.as_view(), name='all_record_job_username'),
    path('all-record-job/diagram/', DiagramWorkSPUView.as_view(), name='all_record_job_diagram'),

    path('create-parameter-detail-spu-<product>_<detail>/', ParametersDetailForSPUCreateView.as_view(), name='create_parameter_detail_spu'),
    path('edit-parameter-detail-spu-<product>_<detail>/', ParametersDetailForSPEditeView.as_view(), name='edit_parameter_detail_spu'),
    path('parameter-detail-spu-<product>-<detail>/', parameters_detail_for_spu_create_or_edit_redirect, name='parameter_detail_spu'),
    path('milling-detail-for-spu-<record>/', MillingDetailForSPUCreateView.as_view(), name='milling_detail_for_cpu'),

    path('plan/product-add-in-plan-complete/', product_add_in_plan_complite, name='product_add_plan_complete'),
    path('plan/product-add-in-plan/', WorkshopPlanCreateView.as_view(), name='product_add_plan'),
    path('plan/add-existing-batch-in-<object>/', WorkshopPlanAddExistingBatchView.as_view(), name='add_existing_batch_in_plan'),
    path('plan/', WorkshopPlanView.as_view(), name='plan'),
    path('plan/<year>-<month>/', WorkshopPlanView.as_view(), name='plan_year_month'),
    path('plan/<year>-<month>/delete-<object>/', WorkshopPlanDeleteView.as_view(), name='delete_object_from_workshopplan'),
    path('plan/update/<id>/', WorkshopPlanUpdateView.as_view(), name='update_object_from_workshopplan'),

    path('plan/<year>-<month>/batch-<id>/ready/', batch_ready, name='batch_ready_in_plan'),
    path('plan/<year>-<month>/batch-<id>/ready_cancel/', batch_cancel_ready, name='batch_cancel_ready_in_plan'),
    path('plan/<year>-<month>/batch-<id>/ready_complete/', batch_ready_comlite, name='batch_ready_complete'),

    # path('plan/warehouse/add-<object>/', WarehouseCreateView.as_view(), name='create_new_record_in_warehouse'),
    # path('plan/warehouse/new-record/', WarehouseCreateView.as_view(), name='create_new_record_in_warehouse'),
    path('plan/warehouse/new-record/<product>_<detail>', WarehouseCreateSelectedDetailView.as_view(), name='create_and_view_new_record_in_warehouse'),
    path('plan/warehouse/edit-record/<id>', WarehouseUpdateView.as_view(), name='edit_record_in_warehouse'),
    path('plan/warehouse/delete-record/<id>', WarehouseDeleteView.as_view(), name='delete_record_in_warehouse'),
    path('plan/warehouse/exeption-integrity-error/', exeption_integrity_error, name='exeption_integrity_error'),
    path('plan/warehouse/edit-<object_id>/', WarehouseUpdateView.as_view(), name='edit_object_in_warehouse'), # используется в Plan
    path('plan/warehouse/all-record/<product>_<detail>', WarehouseListView.as_view(), name='all_record_in_warehouse'),
    path('plan/warehouse/view-record/', ViewWarehouseRecord.as_view(), name='view_record_in_warehouse'),

    path('test_view/<username>/<id>/', TimeOfWorkInStage.as_view(), name='order_user_edit_test'),



]



