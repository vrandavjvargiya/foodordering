from django import forms
from ordering.models import Address,Profile

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['user', 'street_address', 'zipcode', 'area', 'city']
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'phone', 'gender']
