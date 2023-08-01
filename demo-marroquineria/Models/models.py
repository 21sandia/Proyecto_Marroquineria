from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin,)
from django.contrib.auth.models import Group
from django.db import models

class States(models.Model):
    name = models.CharField(max_length=30, )

    class Meta:
        db_table = 'status'

class Role(models.Model):
    name = models.CharField(max_length=30)
    groups = models.ManyToManyField(Group, verbose_name='Grupos', blank=True)

    class Meta:
        db_table = 'rol'

class Category(models.Model):
    name = models.CharField(max_length=30, )

    class Meta:
        db_table = 'category'


class TypeProd(models.Model):
    fk_id_category = models.ForeignKey(Category, on_delete=models.CASCADE )
    name = models.CharField(max_length=30, )

    class Meta:
        db_table = 'type_prod'  
        

class Product(models.Model):
    fk_id_state = models.ForeignKey(States, on_delete=models.CASCADE )
    fk_id_type_prod = models.ForeignKey(TypeProd, on_delete=models.CASCADE )
    name = models.CharField(max_length=30, )
    image = models.ImageField(upload_to='media/')
    reference = models.CharField(max_length=60, )
    price = models.DecimalField(max_digits=10, decimal_places=2, )

    class Meta:
        db_table = 'product'


class DetailProd(models.Model):
    fk_id_product = models.ForeignKey(Product, on_delete=models.CASCADE )
    registration_date = models.DateField()
    color = models.CharField(max_length=30, )
    size_p = models.CharField(max_length=50, )
    material = models.CharField(max_length=40, )
    quantity = models.IntegerField()

    class Meta:
        db_table = 'detail_prod'
        
class People(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    document = models.IntegerField()
    date_birth = models.DateField()
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=30)
    gener = models.CharField(max_length=10)
    user_rol = models.ForeignKey(Role, on_delete=models.CASCADE) 
    type_document =models.CharField(max_length=4)
    fk_id_states = models.ForeignKey(States, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'People'
        verbose_name_plural = 'people'
        db_table = 'People'

class User(models.Model):
    fk_id_people = models.ForeignKey(People, on_delete=models.CASCADE)
    fk_id_rol =models.ForeignKey(Role, on_delete=models.CASCADE)
    password = models.CharField(max_length=255)
    class Meta:
        db_table="Users"

class Sale(models.Model):
    date_sale = models.DateField()
    fk_id_people = models.ForeignKey(People, on_delete=models.CASCADE)
    total_sale = models.DecimalField(max_digits=10, decimal_places=2, )
    class Meta:
        db_table = 'sale'

class DetailSale(models.Model):
    fk_id_sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    fk_id_product = models.ForeignKey(Product, on_delete=models.CASCADE )
    customer_name = models.CharField(max_length=50, )
    quantity = models.IntegerField()
    price_unit = models.DecimalField(max_digits=10, decimal_places=2, )
    total_product = models.DecimalField(max_digits=10, decimal_places=2, )
    class Meta:
        db_table = 'detail_sale'

