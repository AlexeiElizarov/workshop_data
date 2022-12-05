from workshop_data.views.batch_views import (
    CreateBatchDetailInPlan,
    AllBatchDetailInPlanView,
    DeleteBatchDetailInPlanView,
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
    WorkerOrdersListForMaster
)
from workshop_data.views.order_views import (
    OrderUserCreateView,
    OrderUserParametrListView,
    OrderUserEditView,
    OrderDeleteView
)
from workshop_data.views.product_view import (
    ProductAllView,
    ProductCreateView,
    ProductAddDetailView,
    ProductDataView
)
from workshop_data.views.detail_view import (
    DetailAllView,
    DetailCreateView
)
from workshop_data.views.complite_view import *
from workshop_data.views.test_views import *
from workshop_data.views.bonus_view import *