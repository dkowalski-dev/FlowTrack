from django.forms import ModelForm

from .models import CompanyClient, IndividualClient
from .utils import formatted_nip, formatted_phone


class IndividualClientForm(ModelForm):
    class Meta:
        model = IndividualClient
        fields = ["name", "last_name", "email", "phone", "address", "region"]
        labels = {
            "name": "Imię",
            "last_name": "Nazwisko",
            "email": "Email",
            "phone": "Telefon",
            "address": "Adres",
            "region": "Region",
        }

    def __init__(self, *arg, **kwargs):
        super(IndividualClientForm, self).__init__(*arg, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        return formatted_phone(phone)


class CompanyClientForm(ModelForm):
    class Meta:
        model = CompanyClient
        fields = [
            "nip",
            "company_name",
            "contact_person",
            "email",
            "phone",
            "address",
            "region",
        ]
        labels = {
            "company_name": "Nazwa firmy",
            "nip": "NIP",
            "contact_person": "Osoba do kontaktu",
            "email": "Email",
            "phone": "Telefon",
            "address": "Adres",
            "region": "Region",
        }

    def __init__(self, *arg, **kwargs):
        super(CompanyClientForm, self).__init__(*arg, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        return formatted_phone(phone)

    def clean_nip(self):
        nip = self.cleaned_data["nip"]
        return formatted_nip(nip)
