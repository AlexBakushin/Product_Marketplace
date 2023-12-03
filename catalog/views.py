from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from catalog.models import Product
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


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
    fields = ('product_name', 'description', 'preview', 'category', 'price')
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.product_name)
            new_mat.save()

        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    fields = ('product_name', 'description', 'preview', 'category', 'price')

    # success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.product_name)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:product', args=[self.kwargs.get('slug')])


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')
