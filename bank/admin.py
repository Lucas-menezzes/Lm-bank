from django.contrib import admin
from bank.models import Clients, Colaborators, Agency

class Client(admin.ModelAdmin):
    list_display = ('id', 'name', 'username', 'email', 'document', 'date_updated')
    list_display_links=('id', 'name')
    search_fields= ('name',)
    list_per_page=15
admin.site.register(Clients, Client)

class Colaborator(admin.ModelAdmin):
    list_display = ('id', 'name', 'registration', 'username', 'email', 'document', 'date_updated')
    list_display_links=('id', 'name')
    search_fields= ('name',)
    list_per_page=15

admin.site.register(Colaborators, Colaborator)

class AgencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount' ,'date_updated')
    search_fields= ('id',)
    list_per_page=15

admin.site.register(Agency, AgencyAdmin)