from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from bank.models import Clients, Colaborators
from bank.models import CustomUser
from ..constants import PROFILE_CHOICES

@api_view(['POST'])
def create_user(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        account = request.data.get('account')
        registration = request.data.get('registration')
        email = request.data.get('email')
        profile = request.data.get('profile')

        if account:
            client = Clients.objects.get(account=account)
            user = client.customuser_ptr if client.customuser_ptr else None
            user.profile = profile
        elif registration:
            colaborator = Colaborators.objects.get(registration=registration)
            user = colaborator.customuser_ptr if colaborator.customuser_ptr else None
            user.profile = profile
        if account and (client.username != username or client.email != email):
            return Response({"detail": "credenciais invalidas."}, status=status.HTTP_400_BAD_REQUEST)
        
        elif registration and(colaborator.username != username or colaborator.email != email):
            return Response({"detail": "credenciais invalidas colaborador."}, status=status.HTTP_400_BAD_REQUEST)
        
        if profile not in dict(PROFILE_CHOICES).keys():
            return Response({"details": "Profile does exist"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()

        return Response({"detail": "Senha atualizada com sucesso"}, status=status.HTTP_200_OK)

    except Clients.DoesNotExist:
        return Response({'detail': 'Cliente não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
    except Colaborators.DoesNotExist:
        return Response({'detail': 'Colaborador não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get(request):
    try:
        users = CustomUser.objects.all()
        
        serialized_users = []

        for user in users:
            serialized_user = {'username': user.username, 'profile': user.profile}
            serialized_users.append(serialized_user)

        return JsonResponse({'users': serialized_users}, status=200)
    except Exception as e:
        return JsonResponse({'errors':str(e)}, status=500)