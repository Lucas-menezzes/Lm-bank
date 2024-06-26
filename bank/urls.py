# from django.contrib import admin
from django.urls import path
from bank.views.create_client import client_list, create_client
from bank.views.create_agency import create_agency, agency_list
from bank.views.create_colaborator import create_colaborator, get_colaborator
from bank.views.create_user import create_user, get
from bank.views.login import ObtainToken
from bank.views.mk_deposit import mk_deposit
from bank.views.mk_withdraw import mk_withdraw

urlpatterns = [

    path('authenticator/', ObtainToken.as_view(), name='authenticator' ),
    path('update_pass/', create_user, name='client-login' ),
    path('get_user/', get, name='get-user' ),

    path('create_client/', create_client, name='create-client'),
    path('list_client/', client_list, name='client-list' ),
    path('list_client/<int:account>', client_list, name='client-list-account' ),

    path('create_agency/', create_agency, name='create-agency'),
    path('list_agency/', agency_list, name='list-agency'),
    path('list_colaborator/', get_colaborator, name='list-colaborator'),
    path('create_colaborator/', create_colaborator, name='create-colaborator'),

    path('mk_deposit/', mk_deposit, name='mk_deposit'),
    path('mk_withdraw/', mk_withdraw, name='mk_withdraw'),
]
