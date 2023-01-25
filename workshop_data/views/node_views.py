import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView

from workshop_data.forms import (
    NodeCreateForm,
    NodeAddDetailForm,
    NodeAddNodeForm)
from workshop_data.models import Node, Detail


class NodeAllView(LoginRequiredMixin, ListView):
    """Отображает страницу со всеми узлами"""
    model = Node
    template_name = "workshop_data/node/nodes_list_all.html"
    context_object_name = "nodes"


class NodeCreateView(LoginRequiredMixin, CreateView):
    """Отображает страницу создания Узла"""
    model = Node
    form_class = NodeCreateForm
    template_name = "workshop_data/node/node_create.html"
    success_url = reverse_lazy('nodes_list_all')

    def get_success_url(self):
        if "save_and_continue" in self.request.POST:
            return reverse('create_new_node')
        return super(NodeCreateView, self).get_success_url()


class NodeAddDetailView(LoginRequiredMixin, UpdateView):
    """Отображает страницу добавления Детали в Узел"""
    model = Node
    form_class = NodeAddDetailForm
    template_name = 'workshop_data/node/node_add_detail.html'
    success_url = reverse_lazy('node_list_all')
    context_object_name = 'node'

    def get_object(self, **kwargs):
        obj = Node.objects.filter(name=self.kwargs.get('node'))
        return obj.first()

    def form_valid(self, form):
        obj = self.get_object()
        for added_detail in form.cleaned_data['detail']:
            obj.detail.add(added_detail)
        if "save_and_continue" in self.request.POST:
            time.sleep(.2)
            return HttpResponseRedirect(reverse('node_add_detail', kwargs={'node': obj.name}))
        return redirect('node_list_all')


class NodeAddNodeView(LoginRequiredMixin, UpdateView):
    """Отображает страницу добавления Узла в Узел"""
    model = Node
    form_class = NodeAddNodeForm
    template_name = 'workshop_data/node/node_add_detail.html'
    success_url = reverse_lazy('node_list_all')
    context_object_name = 'node'

    def get_object(self, **kwargs):
        obj = Node.objects.filter(name=self.kwargs.get('node'))
        return obj.first()
