from django.forms import ModelForm
from .models import IndividualClient, CompanyClient

class IndividualClientForm(ModelForm):
    class Meta:
        model = IndividualClient
        fields = ['name', 'last_name', 'email', 'phone', 'address', 'region' ]
        labels = {
            'name': 'Imię', 
            'last_name': "Nazwisko", 
            'email': "Email", 
            'phone': "Telefon", 
            'address': "Adres", 
            'region': "Region",
        }

    def __init__(self, *arg, **kwargs):
        super(IndividualClientForm, self).__init__(*arg, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

class CompanyClientForm(ModelForm):
    class Meta:
        model = CompanyClient
        fields = ['company_name', 'nip', 'email', 'phone', 'address', 'region' ]
        labels = {
            'company_name': 'Nazwa firmy', 
            'nip': "NIP", 
            'email': "Email", 
            'phone': "Telefon", 
            'address': "Adres", 
            'region': "Region",
        }

    def __init__(self, *arg, **kwargs):
        super(CompanyClientForm, self).__init__(*arg, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})