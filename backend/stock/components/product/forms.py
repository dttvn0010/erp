from django import forms
from django.utils.translation import gettext_lazy as _
from core.utils.forms import ModelForm, AsyncModelChoiceField

from stock.models import Product, ProductCategory
from core.constants import BaseStatus

class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ['company', 'create_date', 'update_date', 'status', 'properties']
    
    category = AsyncModelChoiceField(queryset=ProductCategory.objects.none(),
                    label=_('verbose_name.product.category'))

    description = forms.CharField(required=False, 
                    widget=forms.Textarea({'rows': 5}),
                    label=_('verbose_name.product.category.description'))

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = ProductCategory.objects.filter(
            company=company,
            status=BaseStatus.ACTIVE.name
        )
        