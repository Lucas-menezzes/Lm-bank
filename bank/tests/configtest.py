import pytest
import django
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Faker
from ..views.create_agency import create_agency
from bank.models import Agency, Clients
from datetime import datetime
from rest_framework.response import Response


django.setup()
fake = Faker()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_client_url():
    return reverse('create-client')

@pytest.fixture
def create_colab_url():
    return reverse('create-colaborator')

@pytest.fixture
def data_fakes():
    # age_min = 18
    username= fake.user_name()
    cpf = fake.numerify(text='###########')
    num_account= fake.random_int(min=1000, max=9999)
    registration= fake.random_int(min=100000, max=999999)
    return cpf, username, num_account, registration

@pytest.fixture
def valid_age(request, age_min):
    date_birth = datetime.strptime(request.data['date_birth'], '%Y-%m-%d').date()
    today = datetime.now().date()
    age = today.year - date_birth.year - ((today.month, today.day) < (date_birth.month, date_birth.day))
    if age > age_min:
        return True

@pytest.fixture
def list_agency_url():
    return reverse('list-agency')

@pytest.fixture
def mock_agency(db):
    agency_mok= Agency.objects.create(
        phone="11989898922",
        adress="Rua teste, 23 - São Paulo/SP",
        agency_number=9999
    )
    return agency_mok

@pytest.fixture
def mock_generated_client(db):
    agency = Agency.objects.create(agency_number=9990, adress="Rua teste, 23 - São Paulo/SP", phone="99232332")
    generated_client= Clients.objects.create(
        username="test43e8",
        name="test 42",
        adress="Rua teste",
        email="teste@gmail.com",
        phone="1230932",
        account=1212,
        date_birth="2000-01-01",
        document="00000000191",
        agency_id= agency
    )
    return generated_client