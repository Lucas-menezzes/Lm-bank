from rest_framework import serializers
from bank.models import Clients, Colaborators, Agency

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        exclude = ['password', 'date_created', 'date_updated', 'date_joined']

class ColaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colaborators
        exclude = ['password', 'date_created', 'date_updated', 'date_joined']

class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = '__all__'
        
    def validate_agency_number(self, value):
        if Agency.objects.filter(agency_number=value).exists():
            raise serializers.ValidationError("Este número de agência já está em uso.")
        return value