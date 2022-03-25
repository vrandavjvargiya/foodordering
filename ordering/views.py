
from cProfile import Profile
from http import client
# from email.headerregistry import Address
from multiprocessing import context
# from tkinter import Menu
from unicodedata import name
from unittest import result
from urllib import request

from django.conf import settings
import razorpay
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Item, Cuisine, Address, Order, OrderItem
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.paginator import Paginator
from ordering.models import Item
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib import auth
from django.db.models import Q
# from cart.context_processor import cart_total_amount 

client=razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
def app_create():
    return render('app.html')   

def index(request):
    cuisine_list = Cuisine.objects.all()
    paginator = Paginator(cuisine_list,2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'ordering/index.html', {'page_obj':page_obj})

def showitems(request,cuisine_id):
    item_list = Item.objects.filter(cuisine_id=cuisine_id).order_by('name')
    paginator = Paginator(item_list,1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'ordering/items.html', {'page_obj':page_obj, 'c_id':cuisine_id})

def about(request):
    return render(request, 'ordering/about.html')

def contact(request):
    return render(request, 'ordering/contact.html')

def search(request):
    q = request.GET['q']
    allItems = Item.objects.filter(name__icontains=q)
    print(allItems)
    params = {'allItems': allItems}
    return render(request, 'ordering/search.html', params)

# create,update,delete
class AddressCreateView(CreateView):
    model = Address
    template_name = 'ordering/checkout.html'
    success_url = '/placeorder'    
    fields = ['street_address', 'zipcode', 'area', 'city']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(AddressCreateView, self).form_valid(form)
        

class AddressUpdateView(UpdateView):
    model = Address
    fields = ['user', 'street_address', 'zipcode', 'area', 'city']
    template_name_suffix = '_update_address'


class ProfileCreateView(CreateView):
    model = Profile
    fields = ['user', 'phone', 'gender']

class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['user', 'phone', 'gender']
    template_name_suffix = '_update_profile'
    
class ProfileDeleteView(DeleteView):
    model = Profile
    fields = ['user','phone', 'gender']
    
@login_required(login_url="/users/login")
def cart_add(request, id, c_id):
    cart = Cart(request)
    item = Item.objects.get(id=id)
    cart.add(item)
    return redirect("show-items", cuisine_id=c_id)

@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    item = Item.objects.get(id=id)
    cart.remove(item)
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    item = Item.objects.get(id=id)
    cart.add(product=item)
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    item = Item.objects.get(id=id)
    cart.decrement(product=item)
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

@login_required(login_url="/users/login")
def cart_detail(request):
    return render(request, 'ordering/cart_detail.html')   

def checkout(request):
    total = 0.0
    orderlines = []
    for k, item in request.session['cart'].items():
        total += item['quantity']*float(item['price'])
    
    payment = client.order.create({
        "amount": total, 
        "currency": "INR"
    })
    order = Order.objects.create(user=request.user, amount=total, payment_id=payment['id'])
    for k, item in request.session['cart'].items():
        total += item['quantity']*float(item['price'])
        orderlines.append(
            OrderItem(
                item_id=int(item['product_id']),
                quantity=item['quantity'],
                price=item['price'],
                order=order
            )
        )
    objs = OrderItem.objects.bulk_create(orderlines)
    context = {
        'order_id' : payment['id'],
        'total' : total
        }
    
    request.session.get['order_id']=payment['id']
    request.session.get['total']=total
    
    return render(request,'ordering/pay.html',context)
    
def placeorder(request):
    return render(request,'ordering/placeorder.html')

def pay(request):
    return render(request,'ordering/pay.html')
    



