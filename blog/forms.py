from django import forms
from blog.models import Blog


class BlogForm(forms.ModelForm):  # Форма под создание екземпляра продукта

    class Meta:
        model = Blog
        # fields = '__all__' можно так (выбрать все поля)
        fields = ('title', 'body', 'preview')
        # exclude = ('is_active', ...,...)  + это (исключить)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
