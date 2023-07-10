from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager,
    PermissionsMixin,
)

from enum import Enum 
from django.db import models

#  **USER**

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Falta Email')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, )

    class Meta:
        managed = False
        db_table = 'category'


class DetailProd(models.Model):
    id_detail_prod = models.AutoField(primary_key=True)
    fk_id_product = models.ForeignKey('Product', models.DO_NOTHING, db_column='fk_id_product', )
    registration_date = models.DateField()
    color = models.CharField(max_length=30, )
    size_p = models.CharField(max_length=50, )
    material = models.CharField(max_length=40, )
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'detail_prod'


class DetailSale(models.Model):
    id_detail_sale = models.AutoField(primary_key=True)
    fk_id_sale = models.ForeignKey('Sale', models.DO_NOTHING, db_column='fk_id_sale', )
    customer_name = models.CharField(max_length=50, )
    quantity = models.IntegerField()
    price_unit = models.DecimalField(max_digits=10, decimal_places=2, )
    total = models.DecimalField(max_digits=10, decimal_places=2, )

    class Meta:
        managed = False
        db_table = 'detail_sale'


class People(models.Model):
    id_people = models.AutoField(primary_key=True)
    fk_id_rol = models.ForeignKey('Rol', models.DO_NOTHING, db_column='fk_id_rol', )
    fk_id_status = models.ForeignKey('Status', models.DO_NOTHING, db_column='fk_id_status', )
    name = models.CharField(max_length=30, )
    last_name = models.CharField(max_length=30, )
    document = models.IntegerField()
    phone = models.CharField(max_length=10, )
    address = models.CharField(max_length=30, )

    class Meta:
        managed = False
        db_table = 'people'


class Product(models.Model):
    id_product = models.AutoField(primary_key=True)
    fk_id_status = models.ForeignKey('Status', models.DO_NOTHING, db_column='fk_id_status', )
    fk_id_type_prod = models.ForeignKey('TypeProd', models.DO_NOTHING, db_column='fk_id_type_prod', )
    name = models.CharField(max_length=30, )
    image = models.CharField(max_length=500, )
    reference = models.CharField(max_length=60, )
    price = models.DecimalField(max_digits=10, decimal_places=2, )

    class Meta:
        managed = False
        db_table = 'product'


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, )

    class Meta:
        managed = False
        db_table = 'rol'


class Sale(models.Model):
    id_sale = models.AutoField(primary_key=True)
    fk_id_product = models.ForeignKey(Product, models.DO_NOTHING, db_column='fk_id_product', )
    date_sale = models.DateField()
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2, )

    class Meta:
        managed = False
        db_table = 'sale'


class Status(models.Model):
    id_status = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, )

    class Meta:
        managed = False
        db_table = 'status'


class TypeProd(models.Model):
    id_type_prod = models.AutoField(primary_key=True)
    fk_id_category = models.ForeignKey(Category, models.DO_NOTHING, db_column='fk_id_category', )
    name = models.CharField(max_length=30, )

    class Meta:
        managed = False
        db_table = 'type_prod'
