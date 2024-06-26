from bank.models import Clients, Agency
from ..serializers import ClientSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..schemas import CreateClient
from pydantic import ValidationError
from datetime import datetime
from ..validators.utils import valid_age, document_exist
from django.contrib.auth.decorators import permission_required


@api_view(['POST'])
def create_client(request):
    '''Cria um cliente'''
    try:      
        data = request.data
        date_birth = datetime.strptime(data['date_birth'], '%Y-%m-%d').date()
        # Verificar se todos os campos obrigatórios estão presentes e não estão vazios
        required_fields = ['username', 'name', 'client_email', 'account', 'date_birth', 'document', 'agency']
        for field in required_fields:
            if field not in data or not data[field]:
                return Response({"detail": f"O campo {field} não pode estar vazio."}, status=status.HTTP_400_BAD_REQUEST)
        #valida a idade minima do cliente
        if not valid_age(date_birth, 18):
            return Response({'detail': str.format("Cliente deve ser maior de idade.")}, status=status.HTTP_400_BAD_REQUEST)
        
        if document_exist(Clients, 'document', data['document']):
            return Response({'detail': str.format("Cpf ja cadastrado.")}, status=status.HTTP_400_BAD_REQUEST)
        #username Existe?
        if document_exist(Clients, 'username', data['username']):
            return Response({'detail': str.format("Username ja cadastrado.")}, status=status.HTTP_400_BAD_REQUEST)

        if Clients.objects.filter(account=data['account']).exists():
            return Response({'detail': str.format("Conta ja cadastrado.")}, status=status.HTTP_400_BAD_REQUEST)
       
        payload = CreateClient(**request.data)
        agency = Agency.objects.get(agency_number=payload.agency)  # Encontra a agência correspondente ao número fornecido

        new_client=Clients.objects.create(**payload.model_dump(exclude={'agency'}), agency_id=agency)
        new_client.save()

        response_data = payload.model_dump(mode='json', exclude={'username', 'password'})
        response_data['message'] = 'Please, create a new user for client'
        
        return Response(response_data, status=status.HTTP_201_CREATED)    
    except Agency.DoesNotExist:
        return Response({"detail": "A agência não existe."}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError as validation_error:
        return Response({"detail": str(validation_error)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as exception:
        return Response({"detail": str(exception)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def client_list(request, account=None):    ##'''Retorna todos os clientes'''
    
    if account is not None:
        try:
            client = Clients.objects.get(account=account)
            serializer = ClientSerializer(client)
            return Response(serializer.data)
        except ClientSerializer.DoesNotEx:
            return Response({"detail":"Cliente não existe"})
    
    clients = Clients.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)