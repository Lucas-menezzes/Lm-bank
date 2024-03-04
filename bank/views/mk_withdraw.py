from bank.models import Withdraw, Deposit, Clients, Agency
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..schemas import CreateWithdraw
from pydantic import ValidationError
from datetime import datetime
from decimal import Decimal
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@api_view(['POST'])
@login_required
def mk_withdraw(request):
    try:
        user= request.user
        payload = CreateWithdraw(**request.data)   
        account = payload.account
        withdraw_value = Decimal(request.data['value'])
        #valida campo conta vazio
        if not account:
            return Response({'details': 'Preencha o campo conta'}, status=status.HTTP_400_BAD_REQUEST)        
        try:
            client = Clients.objects.get(account=account)
        except Clients.DoesNotExist:
            return Response({'details': "A conta não existe"}, status=status.HTTP_404_NOT_FOUND)
        try:
            agency = Agency.objects.get(agency_number=payload.agency)
        except Agency.DoesNotExist:
            return Response({'details': "Agênica não existe"}, status=status.HTTP_404_NOT_FOUND)        
        if client.agency_id_id != agency.id:
            return Response({'details': "Agencia não pertence a essa conta"}, status=status.HTTP_400_BAD_REQUEST)       
        
        if client.customuser_ptr != user:
            return Response({'details': "Você não tem permissão para acessar essa conta"}, status=status.HTTP_403_FORBIDDEN)
        
        if client.balance < payload.value:
            return Response({'details': "Saldo insuficiente"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            client = Clients.objects.select_for_update().get(account=account)
            current_balance = client.balance
            new_balance = current_balance - withdraw_value
            client.balance = new_balance
            client.save()
            
            user_id = client
            
            new_withdraw = Withdraw.objects.create(
                **payload.model_dump(exclude={'agency', 'account', 'value'}),
                user_id=user_id, 
                agency_id=agency,
                account=client,
                value=withdraw_value,
                balance_after= new_balance
                )
            new_withdraw.save()

            return Response({'message':'Saque realizado com sucesso'}, status=status.HTTP_201_CREATED)

    except ValidationError as validation_error:
        return Response({"detail": str(validation_error)}, status=status.HTTP_400_BAD_REQUEST)

