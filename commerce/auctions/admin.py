from django.contrib import admin
from .models import User, createListing, Listing,bidForm,bid, watchlist, commentsForm, comments, Category
# Register your models here.

admin.site.register(Listing),
admin.site.register(bid),
admin.site.register(comments),
admin.site.register(Category)
