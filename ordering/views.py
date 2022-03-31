
from audioop import reverse
from cProfile import Profile
from http import client
from itertools import product
from locale import currency
from multiprocessing import context
from operator import imod
from pickle import TRUE
from unicodedata import name
from unittest import result
from urllib import request, response
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
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.db.models import Q

client=razorpay.Client(auth=('rzp_test_8e8nSfaxDWJutX','1zH3RnQqea9Mns8ld9lbaF96'))

# def payment_status():
#     response=request.Post
#     print (response)
#     return render('success.html')   

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
    return render(request,'ordering/placeorder.html')
    
def placeorder(request):
    total = 0.0
    for key, value in request.session["cart"].items():
        total = total + (float(value["price"]) * value["quantity"])
        total = total
    payment = client.order.create(
        {
            "amount": total*100,
            "currency": "INR",
            # "payment_capture": "1",
        }
    )
    # print(total_pay)
    order_id = payment["id"]
    payment_id=payment["id"]
    oid = request.session.get("order_id")
    print(oid)
    context = {"order_id": order_id, "total_money": total,"payment_id":payment_id}
    order = Order(
        user=request.user,
        amount=total,
        order_id=oid,
        razorpaypaymentid=payment,
        payment_id=payment_id
    )
    order.save()
    request.session["order_id"] = order.id
    print(request.session["order_id"])

    cart = request.session.get("cart")
    orderitem = []
    for i in cart:
        a = int(cart[i]["price"])
        b = cart[i]["quantity"]
        total = a * b         
        print(total)
        i = OrderItem(
            order=order,
            item=cart[i]["name"],
            quantity=cart[i]["quantity"],
            price=int(cart[i]["price"]),
            total=total,
        )
        orderitem.append(i)
        # i.save()
    OrderItem.objects.bulk_create(orderitem)
    if request.method == "POST":
        print(request)
    return render(request,'ordering/placeorder.html' , context)

@csrf_exempt
def success(request):
    parameter = request.POST.dict()
    if client.utility.verify_payment_signature(parameter):
        order = Order.objects.filter(order_id=parameter["razorpay_order_id"]).first()
        paid = True
        return render(request, "thankyou.html", {"status": True})
    else:
        # TODO : Show payment fail message to user.
        return render(request, "thankyou.html", {"status": False})                    
                    
                    
def thankyou(request):
    return render(request,'ordering/thankyou.html')


