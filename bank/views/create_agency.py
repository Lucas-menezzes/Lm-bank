from bank.models import Agency
from ..serializers import AgencySerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..schemas import CreateAgency, AgencySchema
from pydantic import ValidationError


@api_view(['POST'])
def create_agency(request, **kwargs):
    try:
        payload = CreateAgency(**request.data)
        exist_agency = Agency.objects.filter(agency_number=payload.agency_number).first()
        if exist_agency:
            return Response({"detail": "Uma agência com o mesmo número já existe."})
        
        new_agency = Agency.objects.create(**payload.model_dump())
        new_agency.save()
        return Response(payload.model_dump(mode='json'), status=status.HTTP_201_CREATED)
    except ValidationError as validation_error:
        return Response({'details': str(validation_error)},status=status.HTTP_400_BAD_REQUEST)
    except Exception as exception:
        return Response({"detail": str(exception)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def agency_list(request):
    '''Retorna todas as agencias'''
    agencias = Agency.objects.all()
    agencia_data = AgencySerializer(agencias, many=True)
    return Response(agencia_data.data)
