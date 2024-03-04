import json
from bank.tests.configtest import create_colab_url, mock_generated_client, mock_agency, api_client, create_client_url, data_fakes
from django.urls import reverse


def test_create_colaborator(api_client, mock_agency, create_colab_url, data_fakes, db):
    
    colaborator_data = {
        "username":data_fakes[1],
        "name":"Test name",
        "adress":"Rua B, 8- Salvador/BA",
        "email":"teste223@email.com",
        "registration": data_fakes[2],
        "phone": "899998888",
        "date_birth":"2001-01-01",
        "document":data_fakes[0],
        "agency": mock_agency.agency_number,
        "nivel":"B"
    }
    json_data = json.dumps(colaborator_data)
    response = api_client.post(create_colab_url, data=json_data, content_type='application/json')
    response_data = response.json()
    assert response.status_code == 201
    assert response_data is not None

def test_age_colab(api_client, mock_agency, create_colab_url, data_fakes, db):
    
        colabab_data = {
            "username":data_fakes[1],
            "name":"Test name",
            "adress":"Rua B, 8- Salvador/BA",
            "email":"teste223@email.com",
            "registration": data_fakes[2],
            "phone": "899998888",
            "date_birth":"2010-01-01",
            "document":data_fakes[0],
            "agency": mock_agency.agency_number,
            "nivel":"B"
        }

        json_data = json.dumps(colabab_data)
        response = api_client.post(create_colab_url, data=json_data, content_type='application/json')
        response_data = response.json()
        assert response.status_code == 400
        assert response_data['detail'] == "Colaborador deve ser maior de idade."
      