from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, parser_classes # 🛑 AÑADIDO parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser # 🛑 NUEVO: Para manejar archivos (fotos)
from .serializers import HerramientaSerializer, RegistroUsoSerializer # 🛑 NUEVO: Importar Serializers
from .models import Herramienta, Profile, LoginChallenge 
from django.contrib.auth.models import User
import random

# ------------------- VISTAS DE AUTENTICACIÓN EXISTENTES -------------------

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'message': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    user = authenticate(username=user.username, password=password)
    if not user:
        return Response({'message': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

    otp = str(random.randint(100000, 999999))
    challenge = LoginChallenge.objects.create(user=user, otp=otp)

    print(f"[DEBUG OTP] Enviar OTP a {user.email}: {otp}") 

    return Response({'challenge': str(challenge.challenge)}, status=status.HTTP_200_OK)


@api_view(['POST'])
def verify_otp(request):
    challenge_id = request.data.get('challenge')
    code = request.data.get('code')

    try:
        challenge = LoginChallenge.objects.get(challenge=challenge_id)
    except LoginChallenge.DoesNotExist:
        return Response({'message': 'Challenge inválido'}, status=status.HTTP_404_NOT_FOUND)

    if not challenge.is_valid():
        return Response({'message': 'OTP expirado'}, status=status.HTTP_400_BAD_REQUEST)

    if challenge.otp != code:
        return Response({'message': 'OTP incorrecto'}, status=status.HTTP_401_UNAUTHORIZED)

    user_data = {
        "id": challenge.user.id,
        "email": challenge.user.email,
        "username": challenge.user.username
    }

    return Response({'message': 'Login exitoso', 'user': user_data}, status=status.HTTP_200_OK)


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

    username = email.split('@')[0] 

    user = User.objects.create_user(username=username, email=email, password=password, first_name=name)
    
    return Response({'message': 'Usuario registrado con éxito'}, status=status.HTTP_201_CREATED)

# ------------------- VISTAS DE HERRAMIENTAS MODIFICADAS/NUEVAS -------------------

# 🛑 FUNCIÓN MODIFICADA: Ahora usa Serializers y maneja fotos
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser]) # Permite recibir archivos y data de formulario
def registrar_herramienta(request):
    """
    Vista para manejar el POST y guardar una nueva Herramienta, incluyendo foto y descripción.
    """
    serializer = HerramientaSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        # Retorna los datos serializados, incluyendo la URL de la foto (si se subió)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🛑 FUNCIÓN NUEVA: Para registrar el uso después del escaneo del QR
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser]) # Permite recibir archivos y data de formulario (foto de evidencia)
def registrar_uso(request):
    """
    Guarda el registro de uso (escaneo del QR) incluyendo la foto de evidencia.
    """
    # Nota: Asegúrate de que el 'herramienta' y 'usuario' se envíen como IDs en el body
    serializer = RegistroUsoSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Registro de uso guardado con éxito', 'data': serializer.data}, 
                          status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
