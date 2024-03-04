from bank.models import Withdraw, Deposit, Clients, Agency
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bank.validators.utils import update_amount
from ..schemas import CreateDeposit
from pydantic import ValidationError
from decimal import Decimal
from django.db import transaction


@api_view(['POST'])
def mk_deposit(request):
    try:

        payload = CreateDeposit(**request.data)   
        agency = Agency.objects.get(agency_number=payload.agency)
        deposit_value = Decimal(request.data['value'])
        name_deposit = request.data['name']
        # valida que o nome foi preenchido
        if not name_deposit:
            return Response({'details': 'Preencha o campo nome'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            client = Clients.objects.get(account=payload.account)
        except Clients.DoesNotExist:
            return Response({'details': "A conta não existe"}, status=status.HTTP_404_NOT_FOUND)

        if client.agency_id_id != agency.id:
            return Response({'details': "Agencia não pertence a essa conta"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
  
                client = Clients.objects.select_for_update().get(account=payload.account)
                #pega o saldo atual e soma com o deposito
                current_balance = client.balance
                new_balance = current_balance + deposit_value
                client.balance = new_balance
                
                #atualiza saldo do cliente no bd
                client.save()
                new_deposit = Deposit.objects.create(
                    **payload.model_dump(exclude={'agency', 'account', 'value'}), 
                    agency_id=agency,
                    account=client, 
                    value=deposit_value,
                    balance_after=new_balance
                )
                new_deposit.save()

                update_amount(agency_number=payload.agency)

        #valida se existe conta no banco
        except Clients.DoesNotExist:
            return Response({'details': "Conta não existe"}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message':'Depósito realizado com sucesso'}, status=status.HTTP_201_CREATED)
    except Agency.DoesNotExist:
        return Response({'details':'Agência não existe'})
    except ValidationError as validation_error:
        return Response({"detail": str(validation_error)}, status=status.HTTP_400_BAD_REQUEST)