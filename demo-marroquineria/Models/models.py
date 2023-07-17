from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin,)
from django.contrib.auth.models import Group
from django.db import models



class Status_g(models.Model):
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
    fk_id_status = models.ForeignKey(Status_g, on_delete=models.CASCADE )
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

class Sale(models.Model):
    fk_id_product = models.ForeignKey(Product, on_delete=models.CASCADE )
    date_sale = models.DateField()
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2, )

    class Meta:
        db_table = 'sale'

class DetailSale(models.Model):
    fk_id_sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=50, )
    quantity = models.IntegerField()
    price_unit = models.DecimalField(max_digits=10, decimal_places=2, )
    total = models.DecimalField(max_digits=10, decimal_places=2, )

    class Meta:
        db_table = 'detail_sale'


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Falta Email')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        #Asignar grupo despues de crear el usuario
        if 'groups' in extra_fields:
            user.user_rol.groups.set(extra_fields['groups'])

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

    user_rol = models.ForeignKey(Role, on_delete=models.CASCADE)
    fk_id_status = models.ForeignKey(Status_g, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=30)
    document = models.IntegerField()
    date_birth = models.DateField()
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=30)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'user'
        db_table = 'user'



