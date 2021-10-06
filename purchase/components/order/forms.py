from django import forms
from django.utils.translation import gettext as _
from core.utils.forms import ModelForm, AsyncModelChoiceField
from core.models import Partner
from core.constants import PartnerType
from purchase.models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields= ['supplier', 'note']

    note = forms.CharField(required=False, 
                    label=_('verbose_name.purchase.order.note'),
                    widget=forms.Textarea({'rows': 5}))
    
    supplier = AsyncModelChoiceField(queryset=Partner.objects.none(),
                    label=_('verbose_name.purchase.order.supplier'))

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super().__init__(*args, **kwargs)

        self.fields['supplier'].queryset = Partner.objects.filter(
            company=company,
            partner_type=PartnerType.COMPANY.name
        )