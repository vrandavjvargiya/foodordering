from django.urls import path
from . import views 



urlpatterns = [
path('', views.index, name='index'),
path("about/", views.about, name="AboutUs"),
path("contact/", views.contact, name="ContactUs"),
]