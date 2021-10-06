from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from stock.models import ProductCategory
from core.constants import BaseStatus
from core.utils.forms import ModelForm, AsyncModelChoiceField

class ProductCategoryForm(ModelForm):
    class Meta:
        model = ProductCategory
        exclude = ['company', 'create_date', 'update_date', 'status']

    parent = AsyncModelChoiceField(queryset=ProductCategory.objects.none(),
                    label=_('verbose_name.product.category.parent'))

    description = forms.CharField(required=False, 
                    widget=forms.Textarea({'rows': 5}),
                    label=_('verbose_name.product.category.description'))

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super().__init__(*args, **kwargs)

        queryset = ProductCategory.objects.filter(
                company=company, 
                status=BaseStatus.ACTIVE.name)

        instance = kwargs.get('instance')
        if instance:
            queryset = queryset.filter(~Q(id=instance.id))

        self.fields['parent'].queryset = queryset