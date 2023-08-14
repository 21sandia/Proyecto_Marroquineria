from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password


class Rol(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'rol'


class States(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'states'


class Peoples(models.Model):
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    type_document = models.CharField(max_length=30)
    document = models.IntegerField()
    gender = models.CharField(max_length=30)
    date_birth = models.DateField()
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=30)

    class Meta:
        db_table = 'peoples'


class Users(models.Model):
    fk_id_state = models.ForeignKey(States, models.DO_NOTHING, db_column='fk_id_state')
    fk_id_rol = models.ForeignKey(Rol, models.DO_NOTHING, db_column='fk_id_rol')
    fk_id_people = models.ForeignKey(Peoples, models.DO_NOTHING, db_column='fk_id_people')
    password = models.CharField(max_length=100)
    last_login = models.DateTimeField(null=True, blank=True, default=timezone.now)

    class Meta:
        db_table = 'users'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def get_email_field_name(self):
        return 'fk_id_people__email'


class Categorys(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'categorys'


class TypeProds(models.Model):
    fk_id_category = models.ForeignKey(Categorys, models.DO_NOTHING, db_column='fk_id_category')
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'type_prods'


class Products(models.Model):
    fk_id_state = models.ForeignKey(States, models.DO_NOTHING, db_column='fk_id_state')
    fk_id_type_prod = models.ForeignKey(TypeProds, models.DO_NOTHING, db_column='fk_id_type_prod')
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='media/', blank=True,  null=True)
    reference = models.CharField(max_length=60)
    description = models.CharField(max_length=1000)
    quantity = models.IntegerField(default=0)
    price_shop = models.DecimalField(max_digits=10, decimal_places=2)
    price_sale = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'products'



class DetailProds(models.Model):
    fk_id_product = models.OneToOneField(Products, on_delete= models.CASCADE, db_column='fk_id_product')
    date = models.DateField(auto_now_add=True)
    color = models.CharField(max_length=30)
    size_p = models.CharField(max_length=50)
    material = models.CharField(max_length=40)

    class Meta:
        db_table = 'detail_prods'


class Sales(models.Model):
    fk_id_state = models.ForeignKey(States, models.DO_NOTHING, db_column='fk_id_state')
    fk_id_people = models.ForeignKey(Peoples, models.DO_NOTHING, db_column='fk_id_people')
    date = models.DateField(auto_now_add=True)
    total_sale = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'sales'


class DetailSales(models.Model):
    fk_id_sale = models.ForeignKey(Sales, models.DO_NOTHING, db_column='fk_id_sale')
    fk_id_prod = models.ForeignKey(Products, models.DO_NOTHING, db_column='fk_id_prod')
    quantity = models.IntegerField()
    price_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_product = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detail_sales'

