from clients.models import CompanyClient, IndividualClient
from django.contrib.contenttypes.models import ContentType
from django.forms import (
    CheckboxSelectMultiple,
    ChoiceField,
    ModelForm,
    ModelMultipleChoiceField,
)
from offers.models import Note, Offer, OfferProduct, Status
from products.models import Product


class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = ["name", "type"]
        labels = {"name": "Nazwa", "type": "Rodzaj statusu"}

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ["status", "description"]
        labels = {"description": "Główny opis oferty"}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        if user:
            self.fields["status"].queryset = Status.objects.filter(owner=user)

            individual_clients = IndividualClient.objects.filter(owner=user)
            company_clients = CompanyClient.objects.filter(owner=user)

            choices = [("", "Wybierz klienta")]
            choices += [
                (str(client.id), client.company_name)
                for client in company_clients
                if client.company_name
            ]
            choices += [
                (str(client.id), f"{client.name} {client.last_name}")
                for client in individual_clients
                if client.name and client.last_name
            ]

            self.fields["client"] = ChoiceField(choices=choices)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        offer = super().save(commit=False)
        if self.user:
            offer.owner = self.user

        client_id = self.cleaned_data.get("client")

        if client_id:
            client = IndividualClient.objects.filter(id=client_id).first()
            if client:
                offer.client_type = ContentType.objects.get_for_model(IndividualClient)
            else:
                client = CompanyClient.objects.filter(id=client_id).first()
                if client:
                    offer.client_type = ContentType.objects.get_for_model(CompanyClient)
                else:
                    offer.client_type = None
            offer.client_id = client.id if client else None

        if commit:
            offer.save()
        return offer


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ["content"]

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


class ProductForm(ModelForm):
    class Meta:
        model = OfferProduct
        fields = ["offer_price", "quantity"]

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})
