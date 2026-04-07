from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from .auth import decode_token

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        token = auth_header.split(' ')[1]
        user_id = decode_token(token)
        if not user_id:
            raise AuthenticationFailed('Invalid token')
        try:
            user = User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
        return (user, None)