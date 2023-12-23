from django import forms
from catalog.models import Product, Version


class ProductForm(forms.ModelForm):  # Форма под создание екземпляра продукта

    class Meta:
        model = Product
        # fields = '__all__' можно так (выбрать все поля)
        fields = ('product_name', 'description', 'preview', 'category', 'price')
        # exclude = ('is_active', ...,...)  + это (исключить)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_product_name(self):
        cleaned_data = self.cleaned_data['product_name']
        banned_names = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        if cleaned_data.lower() in banned_names:
            raise forms.ValidationError('Название является не корректным')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        banned_names = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        if cleaned_data.lower() in banned_names:
            raise forms.ValidationError('Описание является не корректным')

        return cleaned_data


class VersionForm(forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'
        exclude = ('product',)

