# Generated by Django 4.2.7 on 2024-01-19 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_product_options_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.CharField(default='575560846715', max_length=150, unique=True, verbose_name='slug'),
        ),
    ]
