from django.forms import ModelForm
from .models import Category, Product
from django.core.exceptions import ValidationError

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'vat']
        labels = {
            'name': 'Nazwa',
            'vat': 'Stawka VAT'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['serial_number', 'name', 'description', 'category', 'purchase_price', 'sale_price']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.user = user
        if user:
            self.fields['category'].queryset = Category.objects.filter(owner=user)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        product = super().save(commit=False)
        product.owner = self.user
        if commit:
            product.save()
        return product
    
    def clean_sale_price(self):
        if self.cleaned_data['purchase_price'] > self.cleaned_data['sale_price']:
            raise ValidationError("Cena sprzedaży nie może być niższa niż cena zakupu")
        return self.cleaned_data['sale_price']