
from cProfile import Profile
from email.headerregistry import Address
# from re import template
# from turtle import title
from unittest import result
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Item, Cuisine
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.paginator import Paginator
from ordering.models import Item
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib import auth
from django.db.models import Q


     
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


# def search(request):
#     return HttpResponse("We are at search")

# create,update,delete
class AddressCreateView(CreateView):
    model = Address
    fields = ['user', 'street_address', 'zipcode', 'area', 'city']

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

def search(request):
    q = request.GET['q']
    allItems = Item.objects.filter(name__icontains=q)
    print(allItems)
    params = {'allItems': allItems}
    return render(request, 'ordering/search.html', params)

