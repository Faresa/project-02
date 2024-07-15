from django.contrib import admin

from client.models import Address, Client

# Register your models here.
admin.site.register(Client)
admin.site.register(Address)
