from bank.models import Clients, Agency, Colaborators
from ..serializers import  ColaboratorSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..schemas import CreateColaborator
from pydantic import ValidationError
from ..validators.utils import valid_age, document_exist
from datetime import datetime


@api_view(['POST'])
def create_colaborator(request):
    try:
        data = request.data
        date_birth = datetime.strptime(data['date_birth'], '%Y-%m-%d').date()

        if not valid_age(date_birth, 18):
            return Response({'detail': f"Colaborador deve ser maior de idade."}, status=status.HTTP_400_BAD_REQUEST)
        #CPF existe?
        if document_exist(Colaborators, 'document', data['document']):
            return Response({'detail': f"Cpf ja cadastrado."}, status=status.HTTP_400_BAD_REQUEST)
        #username Existe?
        if document_exist(Colaborators, 'username', data['username']):
            return Response({'detail': f"username ja cadastrado."}, status=status.HTTP_400_BAD_REQUEST)

        payload = CreateColaborator(**request.data)
        agency = Agency.objects.get(agency_number=payload.agency)
        new_colaborator = Colaborators.objects.create(**payload.model_dump(exclude={'agency', 'password'}), agency_id=agency)
        new_colaborator.save()

        return Response(payload.model_dump(mode='json'), status=status.HTTP_201_CREATED)
    except Agency.DoesNotExist:
        return Response({"details": "agency não existe"}, status=status.HTTP_404_NOT_FOUND)
    except ValidationError as validation_error:
        return Response({'details': str(validation_error)},status=status.HTTP_400_BAD_REQUEST)
    except Exception as exception:
        return Response({"detail": str(exception)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_colaborator(request):
    colaborator= Colaborators.objects.all()
    serializer = ColaboratorSerializer(colaborator, many=True)
    return Response({'details': serializer.data}, status=status.HTTP_200_OK)