# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class DetailProd(models.Model):
    id_detail_prod = models.AutoField(primary_key=True)
    fk_id_product = models.ForeignKey('Product', models.DO_NOTHING, db_column='fk_id_product', blank=True, null=True)
    registration_date = models.DateField(blank=True, null=True)
    color = models.CharField(max_length=30, blank=True, null=True)
    size_p = models.CharField(max_length=50, blank=True, null=True)
    material = models.CharField(max_length=40, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detail_prod'


class DetailSale(models.Model):
    id_detail_sale = models.AutoField(primary_key=True)
    fk_id_sale = models.ForeignKey('Sale', models.DO_NOTHING, db_column='fk_id_sale', blank=True, null=True)
    customer_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    price_unit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detail_sale'


class People(models.Model):
    id_people = models.AutoField(primary_key=True)
    fk_id_rol = models.ForeignKey('Rol', models.DO_NOTHING, db_column='fk_id_rol', blank=True, null=True)
    fk_id_status = models.ForeignKey('Status', models.DO_NOTHING, db_column='fk_id_status', blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    document = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people'


class Product(models.Model):
    id_product = models.AutoField(primary_key=True)
    fk_id_status = models.ForeignKey('Status', models.DO_NOTHING, db_column='fk_id_status', blank=True, null=True)
    fk_id_type_prod = models.ForeignKey('TypeProd', models.DO_NOTHING, db_column='fk_id_type_prod', blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    reference = models.CharField(max_length=60, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rol'


class Sale(models.Model):
    id_sale = models.AutoField(primary_key=True)
    fk_id_product = models.ForeignKey(Product, models.DO_NOTHING, db_column='fk_id_product', blank=True, null=True)
    date_sale = models.DateField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sale'


class Status(models.Model):
    id_status = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'status'


class TypeProd(models.Model):
    id_type_prod = models.AutoField(primary_key=True)
    fk_id_category = models.ForeignKey(Category, models.DO_NOTHING, db_column='fk_id_category', blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'type_prod'
