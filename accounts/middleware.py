from django.utils.deprecation import MiddlewareMixin
from .auth import decode_token
from .models import User

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            user_id = decode_token(token)
            if user_id:
                try:
                    user = User.objects.get(id=user_id, is_active=True)
                    request.user = user
                    # 👇 ДОБАВЬТЕ ЭТУ СТРОКУ для DRF
                    request._request = request
                except User.DoesNotExist:
                    pass