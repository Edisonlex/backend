from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import UserAccount
from .serializers import UserSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({
                'error': 'Por favor proporciona email y password'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            serializer = UserSerializer(user)
            return Response({
                'user': serializer.data,
                'message': 'Login exitoso'
            }, status=status.HTTP_200_OK)

        return Response({
            'error': 'Credenciales inválidas'
        }, status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "message": "Endpoint de registro de usuarios",
            "instrucciones": "Envía una petición POST con los siguientes campos:",
            "campos_requeridos": {
                "email": "string",
                "username": "string",
                "password": "string"
            }
        }, status=status.HTTP_200_OK)

    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        if not email or not username or not password:
            return Response({
                'error': 'Todos los campos son requeridos'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            if UserAccount.objects.filter(email=email).exists():
                return Response({
                    'error': 'El email ya está registrado'
                }, status=status.HTTP_400_BAD_REQUEST)

            user = UserAccount.objects.create_user(
                email=email,
                username=username,
                password=password
            )

            serializer = UserSerializer(user)
            return Response({
                'user': serializer.data,
                'message': 'Usuario registrado exitosamente'
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        try:
            logout(request)
            return Response({
                'message': 'Sesión cerrada exitosamente'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Error al cerrar sesión'
            }, status=status.HTTP_400_BAD_REQUEST)
