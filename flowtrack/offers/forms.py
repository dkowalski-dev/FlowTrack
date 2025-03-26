from django.forms import ModelForm
from .models import Status

class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = ['name', 'type']
        labels = {
            'name': "Nazwa",
            'type': "Rodzaj statusu"
        }
    def __init__(self, *arg, **kwargs):
        super(StatusForm, self).__init__(*arg, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})