from django.conf import settings
from django.core.cache import cache
from users.models import User
from .models import Category


def get_caches_sellers_for_product(product_slug):
    if settings.CACHE_ENABLED:
        key = f'seller_list_{product_slug}'
        seller_list = cache.get(key)
        if seller_list is None:
            seller_list = User.objects.filter(product__slug=product_slug)
            cache.set(key, seller_list)
    else:
        seller_list = User.objects.filter(product__slug=product_slug)

    return seller_list


def get_caches_categories_for_product(product_slug):
    if settings.CACHE_ENABLED:
        key = f'category_list_{product_slug}'
        category_list = cache.get(key)
        if category_list is None:
            category_list = Category.objects.filter(product__slug=product_slug)
            cache.set(key, category_list)
    else:
        category_list = Category.objects.filter(product__slug=product_slug)

    return category_list
