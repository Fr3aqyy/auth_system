from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import User
from .auth import create_token

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        password2 = request.data.get('password2')
        if password != password2:
            return Response({'error': 'Passwords do not match'}, status=400)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=400)
        user = User(
            email=email,
            first_name=request.data.get('first_name', ''),
            last_name=request.data.get('last_name', ''),
            middle_name=request.data.get('middle_name', '')
        )
        user.set_password(password)
        user.save()
        return Response({'message': 'User created'}, status=201)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email, is_active=True)
            if user.check_password(password):
                token = create_token(user.id)
                return Response({'token': token, 'user_id': user.id})
        except User.DoesNotExist:
            pass
        return Response({'error': 'Invalid credentials'}, status=401)

@method_decorator(csrf_exempt, name='dispatch')
class ProfileView(APIView):
    def get(self, request):
        if not request.user:
            return Response({'error': 'Unauthorized'}, status=401)
        return Response({
            'id': request.user.id,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'middle_name': request.user.middle_name,
            'is_active': request.user.is_active
        })

    def put(self, request):
        if not request.user:
            return Response({'error': 'Unauthorized'}, status=401)
        request.user.first_name = request.data.get('first_name', request.user.first_name)
        request.user.last_name = request.data.get('last_name', request.user.last_name)
        request.user.middle_name = request.data.get('middle_name', request.user.middle_name)
        request.user.save()
        return Response({'message': 'Profile updated'})

    def delete(self, request):
        if not request.user:
            return Response({'error': 'Unauthorized'}, status=401)
        request.user.is_active = False
        request.user.save()
        return Response({'message': 'Account deactivated (soft delete)'})

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    def post(self, request):
        return Response({'message': 'Logged out successfully'})