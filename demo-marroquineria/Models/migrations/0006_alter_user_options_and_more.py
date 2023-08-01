# Generated by Django 4.1.7 on 2023-08-01 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0005_remove_product_fk_id_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.RenameField(
            model_name='detailsale',
            old_name='total',
            new_name='total_product',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='fk_id_status',
            new_name='fk_id_state',
        ),
        migrations.RenameField(
            model_name='sale',
            old_name='total',
            new_name='total_sale',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_rol',
            new_name='fk_id_rol',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='fk_id_product',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='date_birth',
        ),
        migrations.RemoveField(
            model_name='user',
            name='document',
        ),
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
        migrations.RemoveField(
            model_name='user',
            name='fk_id_status',
        ),
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.AddField(
            model_name='detailsale',
            name='fk_id_product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Models.product'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterModelTable(
            name='user',
            table='Users',
        ),
        migrations.RenameModel(
            old_name='Status_g',
            new_name='States',
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('document', models.IntegerField()),
                ('date_birth', models.DateField()),
                ('email', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=30)),
                ('gener', models.CharField(max_length=10)),
                ('type_document', models.CharField(max_length=4)),
                ('fk_id_states', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Models.states')),
                ('user_rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Models.role')),
            ],
            options={
                'verbose_name': 'People',
                'verbose_name_plural': 'people',
                'db_table': 'People',
            },
        ),
        migrations.AddField(
            model_name='sale',
            name='fk_id_people',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Models.people'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='fk_id_people',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Models.people'),
            preserve_default=False,
        ),
    ]
