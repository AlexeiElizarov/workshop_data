from django import forms
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from workshop_data.models.order import Order
from workshop_data.models.stage_manufacturing_detail_in_work import StageManufacturingDetailInWork
from django.http import JsonResponse

from workshop_data.services import get_stage_in_work











