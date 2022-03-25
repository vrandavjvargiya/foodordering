
from cProfile import Profile
from django.contrib import admin
from .models import Cuisine, Item, Order, Address,OrderItem

class OrderItemTubleinline(admin.TabularInline):
    model=OrderItem
    
class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderItemTubleinline]


admin.site.register(Order,OrderAdmin)
admin.site.register(Address)
admin.site.register(Item)
admin.site.register(Cuisine)
admin.site.register(OrderItem)
# admin.site.register(Profile)