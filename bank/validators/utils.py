from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from bank.models import Clients, Agency
# from models import Colaborators, Clients

def valid_age(date_birth, age_min):
    today = datetime.now().date()
    age = today.year - date_birth.year - ((today.month, today.day) < (date_birth.month, date_birth.day))
    if age > age_min:
        return True
    # print(age, age_min, "ERROR: Invalid") 
    
def document_exist(model_class, field_name, field_value):
    if model_class.objects.filter(**{field_name: field_value}).exists():
        return True

def update_amount(agency_number):
    total_amount = Clients.objects.filter(agency_id__agency_number=agency_number).aggregate(total=Sum('balance'))['total']
    agency = Agency.objects.get(agency_number=agency_number)
    agency.amount = total_amount or 0
    agency.save()

# def username_exist(model_class, field_name