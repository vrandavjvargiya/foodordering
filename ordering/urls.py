
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static,settings
from . import views

urlpatterns = [
path("", views.index, name="home"),
path('admin/', admin.site.urls),
path("about/", views.about, name="aboutus"),
path("contact/", views.contact, name="contactus"),
path("items/<int:cuisine_id>", views.showitems, name="show-items"),
path("cart/add/<int:id>/<int:c_id>", views.cart_add, name='cart_add'),
path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
path('search/', views.search, name="search"),
path('cart/checkout/', views.AddressCreateView.as_view(), name="checkout"),
path('conformation', views.checkout, name="conformation"),
path('pay', views.pay, name="pay"),
path('placeorder/', views.placeorder, name="placeorder"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
