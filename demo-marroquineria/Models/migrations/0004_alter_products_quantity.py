# Generated by Django 4.1.7 on 2023-08-04 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0003_alter_products_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='quantity',
            field=models.IntegerField(max_length=1000),
        ),
    ]