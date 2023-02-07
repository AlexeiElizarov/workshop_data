from dal import autocomplete
from django import forms
from django.forms import fields

from workshop_data.models import Detail
from django.core.exceptions import ObjectDoesNotExist


# class NodeCreateForm(forms.ModelForm):
#     """Отображает форму создания нового Узла"""
#     class Meta:
#         model = Node
#         fields = (
#             'prefix',
#             'name',
#             'category'
#         )
#
#         # widgets = {
#         #     'detail': autocomplete.ModelSelect2(url='data_autocomplete_detail'),
#         # }
#
#     def clean(self):
#         name = self.cleaned_data.get('name')
#         if Node.objects.filter(name=name).exists():
#             raise forms.ValidationError(f"Узел {name} уже есть в Базе Данных")


# class NodeAddDetailForm(forms.ModelForm):
#     """Отображает форму добавления Детали в Узел"""
#     # detail = fields.CharField(required=False, widget=forms.Textarea())
#     # detail = forms.ModelMultipleChoiceField(
#     #     queryset=Detail.objects.all()
#     # )
#     class Meta:
#         model = Node
#         fields = (
#             'name',
#             'detail',
#         )
#         widgets = {
#             'detail': autocomplete.ModelSelect2Multiple(url='data_autocomplete_detail'),
#         }

    # def clean(self):
    #     cleaned_data = super(NodeAddDetailForm, self).clean()
    #     # detail = Detail.objects.get(id=int(self.data.get('detail')))
    #     # cleaned_data['detail'] = [detail,]
    #     return cleaned_data


# class NodeAddNodeForm(forms.ModelForm):
#     """Отображает форму добавления Узла в Узел"""
#     class Meta:
#         model = Node
#         fields = (
#             'name',
#             'node',
#         )
#         widgets = {
#             'node': autocomplete.ModelSelect2Multiple(url='data_autocomplete_node'),
#         }