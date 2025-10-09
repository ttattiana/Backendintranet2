from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import LoginChallenge
from django.contrib.auth.models import User
import random

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'message': 'Usuario no encontrado'}, status=404)

    user = authenticate(username=user.username, password=password)
    if not user:
        return Response({'message': 'Credenciales inválidas'}, status=401)

    otp = str(random.randint(100000, 999999))
    challenge = LoginChallenge.objects.create(user=user, otp=otp)

    print(f"[DEBUG OTP] Enviar OTP a {user.email}: {otp}")  # Aquí va integración SMS/email

    return Response({'challenge': str(challenge.challenge)}, status=200)


@api_view(['POST'])
def verify_otp(request):
    challenge_id = request.data.get('challenge')
    code = request.data.get('code')

    try:
        challenge = LoginChallenge.objects.get(challenge=challenge_id)
    except LoginChallenge.DoesNotExist:
        return Response({'message': 'Challenge inválido'}, status=404)

    if not challenge.is_valid():
        return Response({'message': 'OTP expirado'}, status=400)

    if challenge.otp != code:
        return Response({'message': 'OTP incorrecto'}, status=401)

    user_data = {
        "id": challenge.user.id,
        "email": challenge.user.email,
        "username": challenge.user.username
    }

    return Response({'message': 'Login exitoso', 'user': user_data}, status=200)


@api_view(['POST'])
def register_view(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')
    phone = request.data.get('phone')

    if not all([name, email, password, phone]):
        return Response({'message': 'Todos los campos son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'message': 'Email ya registrado'}, status=status.HTTP_400_BAD_REQUEST)

    username = email.split('@')[0]  # Generar username básico

    user = User.objects.create_user(username=username, email=email, password=password, first_name=name)
    
    # Si tienes un modelo perfil para guardar el teléfono, aquí iría la lógica.
    # Por ahora, solo se guarda el usuario con los datos básicos.

    return Response({'message': 'Usuario registrado con éxito'}, status=status.HTTP_201_CREATED)
