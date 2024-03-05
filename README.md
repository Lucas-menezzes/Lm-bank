## API DE BANCO ###
Essa api tem como funções criar clientes, colaboradores de um banco podendo ser feito saque, depósito, saldo. Usando Python, Django e Pydantic. Testes com Pytest


### Usando a API
A api tem as rotas

GET /list_client: Lista todos os clientes cadastrados
GET /list_agency: Lista todas as agencias cadastradas
GET /list_colaborator: Lista todos colaboradores cadastrados

<<<<<<< HEAD
*POST /create_client: Cria o cliente.
*POST /create_colaborator: Cria o colaboradores.
POST /create_agency: Cria a Agencias.
POST /mk_deposit: Faz o deposito na conta do cliente
=======
POST /create_client: Cria o cliente.
POST /create_colaborator: Cria o colaboradores.
POST /create_agency: Cria a Agencias.
POST /mk_deposit: Faz o deposito na conta do cliente.
>>>>>>> 22694f6183bc874021420f22d32c36fa91a9412d
POST /mk_withdraw: Faz o saque do cliente
POST /update_pass: Atutaliza a senha do cliente
POST /authenticator: Faz o Login


## TESTES ###
Antes de executar os testes do pytest deve definir a variavel de ambiente
execute esse comando:
$env:DJANGO_SETTINGS_MODULE = "setup.settings"
