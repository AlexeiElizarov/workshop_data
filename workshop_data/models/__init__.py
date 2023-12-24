from workshop_data.models.product import (
    Product,
    ProductDetail,
    DetailDetail,
    )
from workshop_data.models.detail import Detail, Prefix, ParametersDetailForSPU
from workshop_data.models.stage_manufacturing_detail import StageManufacturingDetail
from workshop_data.models.stage_name import StageName
from workshop_data.models.month import Month
from workshop_data.models.batch_detail_in_plan import BatchDetailInPlan
from workshop_data.models.stage_manufacturing_detail_in_work import StageManufacturingDetailInWork
from workshop_data.models.category_detail import CategoryDetail
from workshop_data.models.comment import Comment
from workshop_data.models.workshop_plan import WorkshopPlan
from workshop_data.models.bonus import Bonus
from workshop_data.models.statement_about_job_over_detail import (
    StatementAboutJobOverDetail,
    ResolutionForStatementAboutJobOverDetail)
from workshop_data.models.order import Order
from workshop_data.models.warehouse import Warehouse, Unit
from workshop_data.models.record_job import RecordJob, EvaluationOfTheOperatorsWork

__all__ = (
    'Product',
    'Detail',
    'Prefix',
    'StageManufacturingDetail',
    'StageName',
    'Month',
    'BatchDetailInPlan',
    'StageManufacturingDetailInWork',
    'CategoryDetail',
    'Comment',
    'WorkshopPlan',
    'Bonus',
    'StatementAboutJobOverDetail',
    'ResolutionForStatementAboutJobOverDetail',
    'Order',
    'Warehouse',
    'Unit',
    'RecordJob',
    'ParametersDetailForSPU',
    'EvaluationOfTheOperatorsWork'
)


