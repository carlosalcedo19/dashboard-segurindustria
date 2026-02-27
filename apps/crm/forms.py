from django import forms
from .models import Client, Lead
from apps.client.models import Company

class UnfoldStyleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-900 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 block w-full sm:text-sm p-2 text-gray-900 dark:text-white'
            })

class ClientForm(UnfoldStyleForm):
    class Meta:
        model = Client
        fields = ['person_type', 'document_type', 'document_number', 'first_name', 'last_name', 'email', 'phone', 'position']

class LeadForm(UnfoldStyleForm):
    class Meta:
        model = Lead
        exclude = ['client','is_active', 'state', 'creator_user', 'product']

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'ruc', 'industry']