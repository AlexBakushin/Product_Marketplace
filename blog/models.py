from django.db import models

NULLABLE = {'blank': True, 'null': True}  # шаблон для необязательного элемента


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    body = models.TextField(verbose_name='содержимое')
    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)
    preview = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
    published_date = models.DateTimeField(auto_now=True, verbose_name='дата публикации')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    view_count = models.IntegerField(default=0, verbose_name='просморы')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
