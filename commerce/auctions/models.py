from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms

class User(AbstractUser):
    pass

class createListing(forms.Form):
    #title for the listing, a text-based description, and what the starting bid should be.
    # Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).
    title = forms.CharField(label="Title", max_length = 500)
    text_description = forms.CharField(label="Text Description",max_length = 2000)
    starting_bid = forms.FloatField(label="Starting bid")
    image_url = forms.CharField(label="Image URL(optional)",max_length=2000,required = False)  # required = false allows this field to be optional
    category = forms.CharField(label="Category(optional)",max_length=20, required = False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

class Category(models.Model):
    catergory_name = models.CharField(max_length=200, null = True)

class Listing(models.Model):
    title = models.CharField(max_length=500)
    text_description = models.CharField(max_length=2000)
    starting_bid = models.FloatField()
    image_url = models.CharField(max_length=2000, blank=True)  # blank=True allows this field to be optional
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,related_name="listings")
    bid= models.FloatField(default= starting_bid)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    lastBidder= models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name="WinnerBidder")
    active = models.BooleanField(default=True)

class bidForm(forms.Form):
    current_bid = forms.FloatField(
        error_messages={
            'invalid': 'The input you provided is invalid, the input should be a number.',
            'required': 'Please enter some data in this field prior submission.',

        })

class bid(models.Model):
    current_bid = models.FloatField()
    listings = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
class watchlist(models.Model):
    listings = models.ManyToManyField(Listing, blank = True, related_name = "watchlists")
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)

class commentsForm(forms.Form):
    Comment = forms.CharField()

class comments(models.Model):
    Comment = models.CharField(max_length=1000, null = True)
    #ensure in views that there is a user signed in
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name="comments")
    #each listing can have several comments but a particular comment can belong to one listing so one to many rlt:
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments',null=True)


