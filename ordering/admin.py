#from unicodedata import category
from django.contrib import admin
from .models import Cuisine, Item, Order, Address

admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Item)
admin.site.register(Cuisine)