from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.forms import inlineformset_factory
from catalog.forms import ProductForm, VersionForm, ModeratorProductForm
from catalog.models import Product, Version
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify
from django.db import transaction
from django.http import Http404
from .services import get_caches_sellers_for_product, get_caches_categories_for_product
from django.http import HttpResponse


class ProductListView(LoginRequiredMixin, ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_staff:
            queryset_pub = queryset.filter(is_published=True)
            queryset_sub = queryset.filter(seller=self.request.user)
            queryset = queryset_pub.union(queryset_sub)
            return queryset
        else:
            return queryset


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.product_name
        context['seller'] = get_caches_sellers_for_product(self.object.slug)
        context['category'] = get_caches_categories_for_product(self.object.slug)
        return context


@login_required
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


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.add_product'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        elif self.request.user.is_staff:
            return False
        else:
            return True

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


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_form_class(self):
        if self.request.user == self.object.seller:
            return ProductForm
        elif self.request.user.groups.filter(name='moderator').exists():
            return ModeratorProductForm
        else:
            return ProductForm

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

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.seller or self.request.user.is_staff:
            return self.object
        elif self.request.user.email != self.object.seller:
            raise Http404


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')
    permission_required = 'catalog.delete_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление "{self.object.product_name}"'
        return context
