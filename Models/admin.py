from django.contrib import admin
from .models import Role, People, Product, Type_prod, Detail_sale, Carts, Category

# Register your models here.

admin.site.register(Role)
admin.site.register(People)
admin.site.register(Detail_sale)
admin.site.register(Carts)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Type_prod)
