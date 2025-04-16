from django.forms import ModelForm
from .models import UserSettings
from clients.utils import formatted_nip, formatted_phone

class UserInfoForm(ModelForm):
    class Meta:
        model = UserSettings
        fields = ['contact_person', 'company_name', 'nip', 'email', 'phone', 'address']
        labels = {
            "contact_person": "Osoba do kontaktu",
            "company_name": "Nazwa firmy",
            "phone": "Telefon",
            "Address": "Adres"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        return formatted_phone(phone)
    
    def clean_nip(self):
        nip = self.cleaned_data['nip']
        return formatted_nip(nip)

class UserPreferencesForm(ModelForm):
    class Meta:
        model = UserSettings
        fields = ['show_created', 'show_client', 'show_description', 'show_client_address', 'show_client_region',
                  'show_client_email', 'show_client_phone', 'show_status',  'default_sort']
        labels = {
            'show_created': "Wyświetlaj datę", 
            'show_client': "Wyświetl nazwę klienta", 
            'show_client_email': "Wyświetl email do kontaktu", 
            'show_client_phone': "Wyświetl numer do kontaktu", 
            'show_client_address': "Wyświetlaj adres",
            'show_client_region': "Wyświetlaj region", 
            'show_status': "Pokaż status", 
            'show_description': "Pokaż opis", 
            'default_sort': "Domyślne sortowanie"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == "default_sort":
                field.widget.attrs.update({"class": "form-control"})
            else:
                field.widget.attrs.update({"class": "form-check-input"})