from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from bank.models import CustomUser


class ObtainToken(APIView):
    def post(self, request, *args, **kwargs):
        username =  request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        print(user)

        if user is not None:
            update_last_login(None, user)  # Chamada para atualizar o last_login
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        else:
            return Response({'detail':'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)