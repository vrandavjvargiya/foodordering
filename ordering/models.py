from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cuisine(models.Model):
    name=models.CharField(max_length=20)
    
    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
       return f"{self.cuisine}: {self.name}"

class Order(models.Model):
    STATUS_CHOICES = (("A",'Accepted'),("P",'Packed'),("OTW",'On The Way'),("Pe",'Pending'),("D",'Delivered'),("C",'Cancelled'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')
    amount = models.CharField(max_length=100)
    status = models.CharField(max_length=3,choices=STATUS_CHOICES,default='Pe')
    ordered_date = models.DateTimeField(auto_now_add=True) 
    payment_id=models.CharField(max_length=200, null=True, blank=True)
    paid=models.BooleanField(default=False,null=True)
    
    
    # def placeorder(self):
    #     self.save()

    def __str__(self):
        return f'{self.user.first_name}' + " " +str(self.payment_id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price=models.CharField(max_length=1000)
    total=models.CharField(max_length=1000)
    
    def __str__(self):
        return self.order.user.username
    
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='address')	
    street_address = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=6, null=True)
    area = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
        
    def __str__(self):
        return f'{self.street_address}'+" , "+self.area


class Profile(models.Model):
    GENDER_CHOICES = (("M",'Male'),("F",'Female'),("O",'Other'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)	
    phone=models.PositiveIntegerField()
    gender=models.CharField(max_length=1,choices=GENDER_CHOICES, null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.first_name}' + " " +self.user.email
