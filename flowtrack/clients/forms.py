from django.forms import ModelForm
from .models import IndividualClient, CompanyClient
from django.core.exceptions import ValidationError

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

    def clean_phone(self):
        formatted_phone = self.cleaned_data['phone']
        if formatted_phone:
            formatted_phone = ''.join(formatted_phone.split())
            if formatted_phone.startswith('+'):
                if formatted_phone[1:].isdigit():
                    if len(formatted_phone) == 12:
                        return formatted_phone[:3] + " " + formatted_phone[3:5] + " " + formatted_phone[5:8] + " " + formatted_phone[8:10] + " " + formatted_phone [10: ]
                    else:
                        raise ValidationError("Długość numeru jest niepoprawna")
            else:
                if formatted_phone.isdigit():
                    if len(formatted_phone) == 9:
                        return ' '.join([formatted_phone[i:i+3] for i in range(0, len(formatted_phone), 3)])
                    else:
                        raise ValidationError("Długość numeru jest niepoprawna")
                else:
                    raise ValidationError("Numer telefonu może zawierać tylko cyfry lub znak '+' przy numerach kierunkowych")
        else:
            return ""


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

    def clean_phone(self):
        formatted_phone = self.cleaned_data['phone']
        if formatted_phone:
            formatted_phone = ''.join(formatted_phone.split())
            if formatted_phone.startswith('+'):
                if formatted_phone[1:].isdigit():
                    if len(formatted_phone) == 12:
                        return formatted_phone[:3] + " " + formatted_phone[3:5] + " " + formatted_phone[5:8] + " " + formatted_phone[8:10] + " " + formatted_phone [10: ]
                    else:
                        raise ValidationError("Długość numeru jest niepoprawna")
            else:
                if formatted_phone.isdigit():
                    if len(formatted_phone) == 9:
                        return ' '.join([formatted_phone[i:i+3] for i in range(0, len(formatted_phone), 3)])
                    else:
                        raise ValidationError("Długość numeru jest niepoprawna")
                else:
                    raise ValidationError("Numer telefonu może zawierać tylko cyfry lub znak '+' przy numerach kierunkowych")
        else:
            return ""