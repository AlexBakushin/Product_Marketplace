from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()

        category1 = Category.objects.create(category_name='fruit', description='fruit')
        category2 = Category.objects.create(category_name='vegetable', description='vegetable')
        category3 = Category.objects.create(category_name='groats', description='groats')

        Product.objects.create(product_name='potato', description='potato', category=category1, price='10',
                               create_date='2023-11-29 11:23')
        Product.objects.create(product_name='apple', description='apple', category=category2, price='12',
                               create_date='2023-11-29 11:23')
        Product.objects.create(product_name='rise', description='rise', category=category3, price='8',
                               create_date='2023-11-29 11:23')

        self.stdout.write(self.style.SUCCESS('Database has been filled with sample data'))
