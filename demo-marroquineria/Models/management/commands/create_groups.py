from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from ...models import Role

class Command(BaseCommand):
    def handle(self, *args, **options):
        # CREA LOS GRUPOS
        group_admin, _ = Group.objects.get_or_create(name='Administrador')
        group_vend, _ = Group.objects.get_or_create(name='Vendedor')
        group_cliente, _ = Group.objects.get_or_create(name='Cliente')

        # OBTENER LOS PERMISOS
        todos_permisos = Permission.objects.all()

        # PERMISOS DEL GRUPO ADMIN
        group_admin.permissions.set(todos_permisos)

        # CREAR Y OBTENER PERMISOS
        permisos_vendedor = Permission.objects.filter(codename__in=['add_category', 'change_category','delete_category', 'view_category',
                                                                    'add_typeprod', 'change_typeprod', 'delete_typeprod', 'view_typeprod', 
                                                                    'add_detailsale', 'view_detailsale', 'add_product', 'change_product', 'delete_product', 'view_product',                            
                                                                    'add_detailprod', 'change_detailprod', 'delete_detailprod', 'view_detailprod', 
                                                                    'add_sale', 'change_sale', 'view_sale', 'add_detailsale', 'change_detailsale', 'view_detailsale'
                                                                    ])
        
        permisos_cliente = Permission.objects.filter(codename__in=['view_category', 'view_typeprod', 'view_product', 'view_detailprod', 'view_sale', 'view_detailsale'])


        # ASIGNAR PERMISOS A LOS GRUPOS
        group_vend.permissions.set(permisos_vendedor)
        group_cliente.permissions.set(permisos_cliente)

        # ASIGNAR GRUPOS A LOS ROLES CORRESPONDIENTES
        rol_admin = Role.objects.get(name='Administrador')
        rol_admin.groups.set([group_admin])

        rol_vendedor = Role.objects.get(name='Vendedor')
        rol_vendedor.groups.set([group_vend])

        rol_cliente = Role.objects.get(name='Cliente')
        rol_cliente.groups.set([group_cliente])

