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
    # image = models.ImageField
    
    def __str__(self):
       return f"{self.cuisine}"
        
   # def get_total_item_(self):
    #    return self.quantity * self.price

class Order(models.Model):
    STATUS_CHOICES = (("A",'Accepted'),("P",'Packed'),("OTW",'On The Way'),("Pe",'Pending'),("D",'Delivered'),("C",'Cancelled'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')
    amount = models.IntegerField()
    status = models.CharField(max_length=3,choices=STATUS_CHOICES,default='Pe')
    ordered_date = models.DateTimeField(auto_now_add=True,auto_now = False)
    items = models.ManyToManyField(Item)

    def __str__(self):
        return f'{self.user.first_name}' + " " +str(self.order_id)

        
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='address')	
    street_address = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=6, null=True)
    area = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    default = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.street_address}'+" , "+self.area


class Profile(models.Model):
    GENDER_CHOICES = (("M",'Male'),("F",'Female'),("O",'Other'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)	
    phone=models.PositiveIntegerField()
    gender=models.CharField(max_length=1,choices=GENDER_CHOICES, null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.first_name}' + " " +self.user.email
