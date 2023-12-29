from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.forms import inlineformset_factory
from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify
from django.db import transaction


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.product_name
        return context


def contacts(request):
    context = {
        'title': 'Контакты'
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Имя: {name}\nТелефон: {phone}\nСообщение: {message}')
    return render(request, 'catalog/contacts.html', context)


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        self.object = form.save()
        self.object.seller = self.request.user
        self.object.save()
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.product_name)
            new_mat.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация продукта'
        return context


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    def form_valid(self, form):
        """Сохранение данных из формсета"""
        formset = self.get_context_data()['formset']
        if formset is None:
            return super().form_valid(form)
        with transaction.atomic():
            if form.is_valid():
                new_mat = form.save()
                new_mat.slug = slugify(new_mat.product_name)
                new_mat.save()
                self.object = form.save()
                if formset.is_valid():
                    formset.instance = self.object
                    formset.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:product', args=[self.kwargs.get('slug')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['version'] = self.object.version_set.filter(is_active=True).first(),
        VersionFormset = inlineformset_factory(self.model, Version, form=VersionForm, extra=1)
        context_data['title'] = f'Изменение "{self.object.product_name}"'
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление "{self.object.product_name}"'
        return context

