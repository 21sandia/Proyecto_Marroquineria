# Generated by Django 4.1.7 on 2023-06-30 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0003_alter_people_adress_alter_people_document_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='people',
            name='email',
        ),
    ]
