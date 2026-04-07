from django.core.management.base import BaseCommand
from access_control.models import Role, BusinessElement, AccessRule
from accounts.models import User

class Command(BaseCommand):
    help = 'Seeds the database with initial roles, elements, rules and users'

    def handle(self, *args, **options):
        # Roles
        admin_role, _ = Role.objects.get_or_create(name='admin')
        manager_role, _ = Role.objects.get_or_create(name='manager')
        user_role, _ = Role.objects.get_or_create(name='user')
        guest_role, _ = Role.objects.get_or_create(name='guest')

        # Business elements
        users_el, _ = BusinessElement.objects.get_or_create(name='users')
        products_el, _ = BusinessElement.objects.get_or_create(name='products')
        orders_el, _ = BusinessElement.objects.get_or_create(name='orders')
        rules_el, _ = BusinessElement.objects.get_or_create(name='access_rules')

        # Admin rules (full access)
        for el in [users_el, products_el, orders_el, rules_el]:
            AccessRule.objects.update_or_create(
                role=admin_role, element=el,
                defaults={
                    'can_read': True, 'can_read_all': True, 'can_create': True,
                    'can_update': True, 'can_update_all': True,
                    'can_delete': True, 'can_delete_all': True
                }
            )

        # Manager rules
        AccessRule.objects.update_or_create(
            role=manager_role, element=products_el,
            defaults={'can_read': True, 'can_read_all': True, 'can_create': True,
                      'can_update': True, 'can_update_all': True, 'can_delete': True, 'can_delete_all': False}
        )
        AccessRule.objects.update_or_create(
            role=manager_role, element=orders_el,
            defaults={'can_read': True, 'can_read_all': True, 'can_create': True,
                      'can_update': True, 'can_update_all': True, 'can_delete': False, 'can_delete_all': False}
        )

        # User rules
        AccessRule.objects.update_or_create(
            role=user_role, element=products_el,
            defaults={'can_read': True, 'can_read_all': True, 'can_create': False,
                      'can_update': False, 'can_update_all': False, 'can_delete': False, 'can_delete_all': False}
        )
        AccessRule.objects.update_or_create(
            role=user_role, element=orders_el,
            defaults={'can_read': True, 'can_read_all': False, 'can_create': True,
                      'can_update': True, 'can_update_all': False, 'can_delete': True, 'can_delete_all': False}
        )

        # Guest rules
        AccessRule.objects.update_or_create(
            role=guest_role, element=products_el,
            defaults={'can_read': True, 'can_read_all': True, 'can_create': False,
                      'can_update': False, 'can_update_all': False, 'can_delete': False, 'can_delete_all': False}
        )

        # Create admin user
        if not User.objects.filter(email='admin@example.com').exists():
            admin = User(
                email='admin@example.com',
                first_name='Admin',
                last_name='Adminov',
                role=admin_role
            )
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Admin user created: admin@example.com / admin123'))

        # Create regular user
        if not User.objects.filter(email='user@example.com').exists():
            user = User(
                email='user@example.com',
                first_name='John',
                last_name='Doe',
                role=user_role
            )
            user.set_password('user123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Regular user created: user@example.com / user123'))

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))