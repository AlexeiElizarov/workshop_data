from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from workshop_data.models.order import Order


def index(request):
    return render(request, 'workshop_data/test.html')

class OrderBlankView(DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'workshop_data/templates/workshop_data/test.html'

















