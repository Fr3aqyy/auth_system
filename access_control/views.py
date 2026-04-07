from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Role, BusinessElement, AccessRule
from .permissions import check_permission

@method_decorator(csrf_exempt, name='dispatch')
class MockProductsView(APIView):
    def get(self, request):
        if not request.user:
            return Response({'error': 'Unauthorized'}, status=401)
        if not check_permission(request.user, 'products', 'read'):
            return Response({'error': 'Forbidden'}, status=403)
        return Response({
            'products': [
                {'id': 1, 'name': 'Laptop', 'price': 1200},
                {'id': 2, 'name': 'Mouse', 'price': 25}
            ]
        })

    def post(self, request):
        if not request.user:
            return Response({'error': 'Unauthorized'}, status=401)
        if not check_permission(request.user, 'products', 'create'):
            return Response({'error': 'Forbidden'}, status=403)
        return Response({'message': 'Product created (mock)'}, status=201)

@method_decorator(csrf_exempt, name='dispatch')
class MockOrdersView(APIView):
    def get(self, request):
        if not request.user:
            return Response({'error': 'Unauthorized'}, status=401)
        if not check_permission(request.user, 'orders', 'read'):
            return Response({'error': 'Forbidden'}, status=403)
        return Response({'orders': [{'id': 1, 'total': 250}]})

@method_decorator(csrf_exempt, name='dispatch')
class AccessRuleAdminView(APIView):
    def get(self, request):
        if not request.user:
            return Response({'error': 'Unauthorized'}, status=401)
        if not check_permission(request.user, 'access_rules', 'read_all'):
            return Response({'error': 'Forbidden'}, status=403)
        rules = AccessRule.objects.select_related('role', 'element').all()
        data = [{
            'id': r.id,
            'role': r.role.name,
            'element': r.element.name,
            'can_read': r.can_read,
            'can_read_all': r.can_read_all,
            'can_create': r.can_create,
            'can_update': r.can_update,
            'can_update_all': r.can_update_all,
            'can_delete': r.can_delete,
            'can_delete_all': r.can_delete_all
        } for r in rules]
        return Response(data)

    def post(self, request):
        if not request.user:
            return Response({'error': 'Unauthorized'}, status=401)
        if not check_permission(request.user, 'access_rules', 'create'):
            return Response({'error': 'Forbidden'}, status=403)
        role_name = request.data.get('role')
        element_name = request.data.get('element')
        try:
            role = Role.objects.get(name=role_name)
            element = BusinessElement.objects.get(name=element_name)
            rule, created = AccessRule.objects.update_or_create(
                role=role, element=element,
                defaults={k: request.data.get(k, False) for k in [
                    'can_read', 'can_read_all', 'can_create',
                    'can_update', 'can_update_all',
                    'can_delete', 'can_delete_all'
                ]}
            )
            return Response({'message': 'Rule created/updated', 'id': rule.id})
        except (Role.DoesNotExist, BusinessElement.DoesNotExist):
            return Response({'error': 'Role or element not found'}, status=400)