from django.db import models

NULLABLE = {'blank': True, 'null': True}  # шаблон для необязательного элемента


class Category(models.Model):
    category_name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return f'{self.category_name}'

    class Meta:
        verbose_name = 'Категория'  # В единственном числе
        verbose_name_plural = 'Категории'  # Во множественном числе


class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='product/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    price = models.IntegerField(verbose_name='цена')
    create_date = models.DateTimeField(auto_now=True, verbose_name='дата создания')
    change_data = models.DateTimeField(verbose_name='дата последнего изменения', **NULLABLE)
    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)

    def __str__(self):
        return f'{self.slug} {self.product_name}'

    class Meta:
        verbose_name = 'Продукт'  # В единственном числе
        verbose_name_plural = 'Продукты'  # Во множественном числе


class Version(models.Model):
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    version_number = models.IntegerField(verbose_name='номер версии')
    version_name = models.CharField(max_length=100, verbose_name='название версии')
    is_active = models.BooleanField(default=True, verbose_name='текушая версия')

    def __str__(self):
        return f'{self.version_number} {self.version_name}'

    class Meta:
        verbose_name = 'Версию'  # В единственном числе
        verbose_name_plural = 'Версии'  # Во множественном числе

