# Generated by Django 4.2.2 on 2023-06-22 15:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0003_alter_people_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='phone',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(9999999999, message='el número debe tener máximo 10 digitos')]),
        ),
    ]
