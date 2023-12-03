from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import contacts, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('edit/<slug:slug>/', ProductUpdateView.as_view(), name='update_product'),
    path('delete/<slug:slug>/', ProductDeleteView.as_view(), name='delete_product')
]
