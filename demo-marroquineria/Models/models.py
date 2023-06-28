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
            raise ValueError('Ingrese el email')
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


#   **ROL**

class Role(models.Model):  
    name_role = models.CharField(max_length=50)

    def __str__(self) :
        return self.name_role
    
    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Role'
        db_table = 'Role'


#  **PERSONA**

class People(models.Model): 
    p_User = models.ForeignKey(User, on_delete=models.CASCADE) 
    p_Role = models.ForeignKey(Role, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    type_doc = models.CharField(max_length=4)
    document = models.PositiveBigIntegerField()
    email = models.EmailField()
    phone = models.PositiveBigIntegerField(validators=[MinValueValidator(1000000000, message='el número debe tener mínimo 10 digitos'),
                                            MaxValueValidator(9999999999, message='el número debe tener máximo 10 digitos')])
    adress = models.CharField(max_length=60) 
    status = models.BooleanField(default=True)
    
    def __str__(self) :
        return self.p_User.email
    
    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Persona'
        db_table = 'People'
    
# **CATEGORIA**

class Category(models.Model):
    name_category = models.CharField(max_length=50)
    description = models.TextField()
    
    def __str__(self) :
        return self.name_category
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categoria'
        db_table = 'Category'
    
#  **TIPO PRODUCTO**

class Type_prod(models.Model):
    p_Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    color = models.CharField(max_length=20)
    size = models.CharField(max_length=20)
    material = models.CharField(max_length=50)
    dimensions = models.CharField(max_length=20)
    guarantee = models.CharField(max_length=100)

    def __str__(self) :
        return str(self.p_Category)
    
    class Meta:
        verbose_name = 'Tipo_producto'
        verbose_name_plural = 'Tipo_producto'
        db_table = 'Type_prod'


#  **PRODUCTO** 

class Product(models.Model):  
    type_Product = models.ForeignKey(Type_prod, on_delete=models.CASCADE)
    name_product = models.CharField(max_length=50)
    reference = models.BigIntegerField()
    description = models.TextField()
    name_provider = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    registration_date = models.DateField(auto_now_add=True)
    initial_price = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    status = models.BooleanField(default=True)

    def __str__(self) :
        return self.name_product
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Producto'
        db_table = 'Product'


# **ORDEN DE COMPRA**

class OrderStatus(Enum):
    CREATED = 'CREATED'
    PAYED = 'PAYED'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'

class Order(models.Model):
    o_People = models.ForeignKey(People, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[(tag, tag.value) for tag in OrderStatus], default=OrderStatus.CREATED.value)
    shipping_total = models.DecimalField(default=5, max_digits=10, decimal_places=2)
    total = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.o_People.name
    
    class Meta:
        verbose_name = 'Orden_compra'
        verbose_name_plural = 'Ordene_compra'
        db_table = 'Order'
    
# **CARRITO DE COMPRAS**

class Carts(models.Model): 
    c_People = models.ForeignKey(People, null=True, on_delete=models.CASCADE)
    c_Product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    subtotal = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)                         
    total = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.c_People.name
    
    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carrito'
        db_table = 'Carts'


#  **DETALLE VENTAS**

class Detail_sale(models.Model):
    ds_Carts = models.ForeignKey(Carts, on_delete=models.CASCADE)
    date_sale = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()

    def __str__(self) :
        return self.ds_Carts.c_People
    
    class Meta:
        verbose_name = 'Detalle_venta'
        verbose_name_plural = 'Detalle_venta'
        db_table = 'Detail_sale'
    


