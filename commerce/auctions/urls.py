from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListings, name="createListing"),
    path("<int:listing_id>", views.viewListing, name="listing"),
    path("bid/<int:listing_id>", views.Bids, name="bid"),
    path("watchlist", views.showWatchlist, name = "watchlist"),
    path("addToWatchlist/<int:listing_id>", views.addToWatchlist, name = "addToWatchlist"),
    path("removeFromWatchlist/<int:listing_id>", views.removeFromWatchlist, name="removeFromWatchlist"),
    path("close/<int:listing_id>", views.closeListing, name ="close"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.listsInCategory, name="listsInCategory")
]
