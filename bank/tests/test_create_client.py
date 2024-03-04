import json
from bank.tests.configtest import mock_generated_client, mock_agency, api_client, create_client_url, data_fakes
from django.urls import reverse


#Teste cadastro de cliente
def test_create_client(api_client, mock_agency, create_client_url, data_fakes, db):

    client_data = {
        "username":data_fakes[1],
        "name":"Test name",
        "adress":"Rua B, 8- Salvador/BA",
        "email":"teste123@gmail.com",
        "client_email":"teste223@email.com",
        "phone": "899998888",
        "account":data_fakes[2],
        "date_birth":"2001-01-01",
        "document":data_fakes[0],
        "agency": mock_agency.agency_number,
    }
    print(client_data)
    json_data = json.dumps(client_data)
    response = api_client.post(create_client_url, data=json_data, content_type='application/json')
    
    response_data = response.json()
    print(response_data)
    assert response.status_code == 201
    assert response_data is not None

#Campos obrigatórios
def test_field_required(api_client, mock_agency, create_client_url, data_fakes, db):
    fields_required=["username", "name", "adress", "email", "account", "date_birth", "document"]
    for field in fields_required:
        client_data = {
            "username":"",
            "name":"teste 20",
            "adress":"Rua B, 8- Salvador/BA",
            "email":"teste@example.com",
            "client_email":"teste223@email.com",
            "phone": "",
            "account":data_fakes[2],
            "date_birth":"2001-01-01",
            "document":data_fakes[0],
            "agency": mock_agency.agency_number,
        }

        json_data = json.dumps(client_data)
        response = api_client.post(create_client_url, data=json_data, content_type='application/json')
        response_data = response.json()
        assert response.status_code == 400
        if client_data[field] == "":
            assert response_data['detail'] == f"O campo {field} não pode estar vazio."

#Cliente deve ser maior de idade
def test_age_client(api_client, mock_agency, create_client_url, data_fakes, db):
    client_data = {
        "username":data_fakes[1],
        "name":"teste 20",
        "adress":"Rua B, 8- Salvador/BA",
        "email":"teste223@email.com",
        "client_email":"teste223@email.com",
        "phone": "899998888",
        "account":data_fakes[2],
        "date_birth":"2011-01-01",
        "document":data_fakes[0],
        "agency": mock_agency.agency_number,
    }

    json_data = json.dumps(client_data)
    response = api_client.post(create_client_url, data=json_data, content_type='application/json')
    response_data = response.json()
    assert response.status_code == 400
    assert response_data['detail'] == "Cliente deve ser maior de idade."

#Cpf não pode existir
def test_document_exist(api_client, mock_generated_client, mock_agency, create_client_url, data_fakes, db):
    
    client_data = {
        "username":data_fakes[1],
        "name":"teste 20",
        "adress":"Rua B, 8- Salvador/BA",
        "email":"teste223@email.com",
        "client_email":"teste223@email.com",
        "phone": "899998888",
        "account":data_fakes[2],
        "date_birth":"2001-01-01",
        "document":"00000000191",
        "agency": mock_agency.agency_number,
    }
    json_data = json.dumps(client_data)
    response = api_client.post(create_client_url, data=json_data, content_type='application/json')
    response_data = response.json()
    assert response.status_code == 400
    assert response_data['detail'] == "Cpf ja cadastrado."

#Username não pode existir
def test_username_exist(api_client, mock_generated_client, mock_agency, create_client_url, data_fakes, db):
    name_exist = mock_generated_client.username
    client_data = {
        "username": name_exist,
        "name":"teste 20",
        "adress":"Rua B, 8- Salvador/BA",
        "email":"teste223@email.com",
        "client_email":"teste223@email.com",
        "phone": "899998888",
        "account":data_fakes[2],
        "date_birth":"2001-01-01",
        "document":data_fakes[0],
        "agency": mock_agency.agency_number,
    }
    json_data = json.dumps(client_data)
    response = api_client.post(create_client_url, data=json_data, content_type='application/json')
    response_data = response.json()
    assert response.status_code == 400
    assert response_data['detail'] == "Username ja cadastrado."

#Conta não pode existir
def test_account_exist(api_client, mock_generated_client, mock_agency, create_client_url, data_fakes, db):

    client_data = {
        "username": data_fakes[1],
        "name":"teste 20",
        "adress":"Rua B, 8- Salvador/BA",
        "email":"teste223@email.com",
        "client_email":"teste223@email.com",
        "phone": "899998888",
        "account":mock_generated_client.account,
        "date_birth":"2001-01-01",
        "document":data_fakes[0],
        "agency": mock_agency.agency_number,
    }
    json_data = json.dumps(client_data)
    response = api_client.post(create_client_url, data=json_data, content_type='application/json')
    response_data = response.json()
    assert response.status_code == 400
    assert response_data['detail'] == "Conta ja cadastrado."
    
#teste cadastro de bancario
#teste cadastro de Gerente