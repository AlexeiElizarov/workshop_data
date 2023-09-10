from workshop_data.views.batch_views import (
    CreateBatchDetailInPlan,
    AllBatchDetailInPlanView,
    # DeleteBatchDetailInPlanView,
    AllBatchDetailProductInPlan
)
from workshop_data.views.stage_views import (
    StageManufacturingDetailInWorkInPlanView,
    StageManufacturingDetailInWorkView,
    EditStageManufacturingDetailInWorkView,
    EditStageInDetailView,
    StageInDetailView,
    AddStageInDeatailVeiw
)
from workshop_data.views.workshopplan_views import (
    WorkshopPlanView,
    WorkshopPlanCreateView,
    WorkshopPlanDeleteView,
    WorkshopPlanUpdateView
)
from workshop_data.views.master_views import (
    WorkerListView,
    # WorkerOrdersListForMaster
)
from workshop_data.views.order_views import (
    OrderUserCreateView,
    OrderUserParametrListView,
    OrderUserEditView,
    OrderDeleteView,
    AllOrderForAllWorker,
    OrderUserEditMonthView,
)
from workshop_data.views.product_view import (
    ProductAllView,
    ProductCreateView,
    ProductAddDetailView,
    ProductDataView
)
from workshop_data.views.detail_view import (
    DetailAllView,
    DetailCreateView,
    DetailEditView
)
from workshop_data.views.category_detail_views import (
    CreateCategoryDetailView,
)
from workshop_data.views.statement_about_job_over_detail_view import (
    StatementAboutJobOverDetailView
)
from workshop_data.views.warehouse_view import (
    WarehouseCreateView,
    WarehouseUpdateView)

from workshop_data.views.complite_view import *
from workshop_data.views.test_views import *
from workshop_data.views.bonus_view import *
from workshop_data.views.services_view import *

from workshop_data.views.any_view import ShiftTask

from workshop_data.views.record_job_view import (
    RecordJobCreateView,
    AllRecordJobForAllWorker,
    DiagramWorkSPUView,
    ParametersDetailForSPUCreateView,
    ParametersDetailForSPEditeView,
    parameters_detail_for_spu_create_or_edit_redirect,
    RecordJobDeleteView,
    AllRecordJobForWorker,
)
