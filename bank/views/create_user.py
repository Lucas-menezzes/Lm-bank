
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from bank.models import Clients
from bank.models import CustomUser


@api_view(['POST'])
def create_user(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        account = request.data.get('account')
        email = request.data.get('email')

        client = Clients.objects.get(account=account)
        
        if client.username != username:
            return Response({"detail": "username não pertence ao usuário."}, status=status.HTTP_400_BAD_REQUEST)
        
        if client.email != email:
            return Response({"detail": "Email incorreto"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = CustomUser.objects.get_or_create(username=username, email=email)
        
        #user = CustomUser.objects.get(username=username, email=email)
        if not created:
            user.set_password(password)
            user.save()
            return Response({"detail": "Senha atualizada com sucesso"}, status=status.HTTP_200_OK)
        else:
            user.set_password(password)
            user.save()

            client.customuser_ptr = user
            client.save()
            return Response({"detail": "Senha criada"}, status=status.HTTP_201_CREATED)

    except Clients.DoesNotExist:
        return Response({'detail': 'Cliente não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get(request):
    try:
        users = CustomUser.objects.all()
        
        serialized_users = []

        for user in users:
            serialized_user = {'username': user.username}
            serialized_users.append(serialized_user)

        return JsonResponse({'users': serialized_users}, status=200)
    except Exception as e:
        return JsonResponse({'errors':str(e)}, status=500)