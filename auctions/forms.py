
from xml.etree.ElementTree import Comment
from django import forms
from django.core.exceptions import ValidationError
from decimal import Decimal
# from django.contrib.auth import get_user_model  
from django.contrib.auth.forms import UserChangeForm

from .models import Listing, Bid, Comment, User

# User = get_user_model()

class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ('title', 'description', 'starting_bid', 'categories', 'image') 
        labels = {
            'title': 'Item Name:',
            'description': 'Short Description (Include Brand, etc):',
            'starting_bid': "Current price (in USD):",
            'categories': 'Stores:',
            'image': 'Image Upload (Optional):',
        }

class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = ('amount', ) 
        labels = {
            'amount': "Cheaper price found (in USD)",
        }

    def set_minimum_bid(self, value):
        self.minimum_bid = Decimal(value)

    def clean_amount(self):
        value = int(self.cleaned_data['amount'])
        if value > self.minimum_bid: #checks for lower price
            raise ValidationError(f'Price is higher than current price; must be at least ${self.minimum_bid}')
        return value
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', )

from django.contrib.auth.forms import PasswordResetForm
class MyPasswordResetForm(PasswordResetForm):

    def is_valid(self):
        email = self.data['email']
        if sum([1 for u in self.get_users(email)]) == 0:
            self.add_error(None, "Unknown email; try again.")
            return False
        return super().is_valid()
    

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_picture']

    def clean_username(self): #allows username change and checks that it's available
        new_username = self.cleaned_data.get('username')
        if User.objects.exclude(pk=self.instance.pk).filter(username=new_username).exists():
            raise forms.ValidationError("This username is already taken. Please choose a different one.")
        return new_username