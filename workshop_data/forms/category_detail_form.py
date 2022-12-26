from django import forms
from workshop_data.models import CategoryDetail


class CreateCategoryDetailForm(forms.ModelForm):
    """Форма создания новой категории"""
    class Meta:
        model = CategoryDetail
        fields = ('name',)
