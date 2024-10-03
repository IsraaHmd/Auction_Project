from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, createListing, Listing,bidForm,bid, watchlist, commentsForm, comments, Category


def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.exclude(active=False)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def createListings(request):
    if request.method=='POST':
        form1 = createListing(request.POST) #no new keyword
        if form1.is_valid():
            categoryName = form1.cleaned_data['category'].lower()
            categoryEntered, created = Category.objects.get_or_create(catergory_name = categoryName)
            #must later make a way to add it to the listing page, but now just return to a new createListing page
            listing = Listing(
            title=form1.cleaned_data['title'],
            text_description=form1.cleaned_data['text_description'],
            starting_bid=form1.cleaned_data['starting_bid'],
            image_url=form1.cleaned_data['image_url'],
            category= categoryEntered,
            bid= form1.cleaned_data['starting_bid'],
            user = request.user
            )
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/createListing.html",{
                          "form": form1
                          })
    return render(request, "auctions/createListing.html",{
                  "form": createListing()
                  })
def viewListing(request,listing_id):
    listing = Listing.objects.get(pk=listing_id) #listing_id is not an attribute of Listing but it is an input taken from the path in urls.py
    bid_count=listing.bids.count()
    authorityToClose = False
    comments = listing.comments.all()
    if listing.lastBidder == request.user:
        if listing.user == request.user:
            authorityToClose = True
        if listing.active:
            currentBidderMessage = "Your bid is the current bid."
            print(comments)
            return render(request,"auctions/listing.html",{
            "listing":listing, # use : not =
            "bid_count" :bid_count,
            "currentBidderMessage":currentBidderMessage,
            "authorityToClose":authorityToClose,
            "comments": comments
            })
        elif not listing.active:
            currentBidderMessage = "You are the winner of this listing."
            return render(request,"auctions/listing.html",{
            "listing":listing, # use : not =
            "bid_count" :bid_count,
            "currentBidderMessage":currentBidderMessage,
            "authorityToClose":authorityToClose,
            "comments": comments
            })
    #if the current user is the one who created the lsiting then we should return a vairable that shows this is true so that they could have a button to close the listing

    if listing.user == request.user:
        authorityToClose = True
        return render(request,"auctions/listing.html",{
        "listing":listing, # use : not =
        "bid_count" :bid_count,
        "authorityToClose":authorityToClose,
        "comments": comments
        })
    return render(request,"auctions/listing.html",{
        "listing":listing, # use : not =
        "bid_count" :bid_count,
        "comments": comments
    })



def Bids(request,listing_id):
    listing = Listing.objects.get(pk=listing_id)
    currentBidderMessage="Your bid is the current bid."
    if request.user.is_authenticated:
        if request.method=='POST':
            biddingForm = bidForm(request.POST)
            if biddingForm.is_valid():
                currentBid= float(biddingForm.cleaned_data['current_bid'])
                bidsOfListing = listing.bids.all()
                isGreatest = True
                for bd in bidsOfListing:
                    if currentBid < bd.current_bid:
                        #currentBid should be greater than or = all bids
                        isGreatest = False
                        break
                if currentBid >= listing.starting_bid and isGreatest:
                    nowBid = bid(
                            current_bid= currentBid,
                            listings = listing,
                            user = request.user
                        )
                    nowBid.save()
                    listing.bid = nowBid.current_bid
                    listing.lastBidder = nowBid.user
                    listing.save()

                    bid_count=listing.bids.count()
                    return render(request,"auctions/listing.html",{
                            "listing":listing,
                            "bid_count": bid_count,
                            "currentBidderMessage":currentBidderMessage
                            })
                else:
                    #if the user is logged in and it is a post but input is invalid
                    bid_count=listing.bids.count()
                    message = "The bid must be greater or equal to the starting bid and the other bids."
                    return render(request,"auctions/listing.html",{
                    "listing":listing,
                    "bid_count": bid_count,
                    "message": message
                    })
            else:
                #it is a post but form invalid
                bid_count=listing.bids.count()
                return render(request,"auctions/listing.html",{
                    "listing":listing,
                    "bid_count": bid_count,
                    "biddingForm": biddingForm
                    })
        else:
            bid_count=listing.bids.count()
            if listing.lastBidder == request.user:
                return render(request,"auctions/listing.html",{
                "listing":listing,
                "bid_count": bid_count,
                "currentBidderMessage":currentBidderMessage
                })
            #if the user is logged in but it is not a POST request
            return render(request,"auctions/listing.html",{
                "listing":listing,
                "bid_count": bid_count
                })
    else:
        bid_count=listing.bids.count()
        #user is not logged in
        #if the user tries to submit the form without being logged in
        if request.method=='POST':
            message = "Must be logged_in first"
            return render(request,"auctions/listing.html",{
                "listing":listing,
                "message": message,
                "bid_count": bid_count
                })
        else:
            return render(request,"auctions/listing.html",{
                "listing":listing,
                "bid_count": bid_count
                })

def closeListing(request, listing_id):
    """
    If the user is signed in and is the one who created the listing,
    the user should have the ability to “close” the auction from this page, Done
    which makes the highest bidder the winner of the auction
    and makes the listing no longer active.
    If a user is signed in on a closed listing page, and the user has won that auction, the page should say so.
    """
    listing = Listing.objects.get(pk=listing_id)
    # winner = listing.lastBidder
    listing.active = False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
 # in reverse, i want it to apply afterwards what the viewListing functions does so i should provide its path as in urls aka its name in urls and args is for the arguments that it takes

def showWatchlist(request):
    #this function just presents the watchlist
    try:
        Watchlist = watchlist.objects.get(user = request.user)
    except watchlist.DoesNotExist:
        Watchlist = watchlist(user=request.user)
        Watchlist.save()
    listings = Watchlist.listings.all()
    return render(request,"auctions/watchlist.html",{
        "listings": listings
    })

def addToWatchlist(request,listing_id):
    if request.user.is_authenticated:
        listing = Listing.objects.get(pk=listing_id)
        try:
            Watchlist = watchlist.objects.get(user = request.user)
        except watchlist.DoesNotExist:
            Watchlist = watchlist(user=request.user)
            Watchlist.save()
        #now that we have the watchlist and the list, add the list to the watchlist and render the page providing it with all the listings in the watchlist
        Watchlist.listings.add(listing)
        Watchlist.save()
        listings = Watchlist.listings.all() # not .objects.all()
        return render(request,"auctions/watchlist.html",{
            "listings": listings
        })

    else:
        message = "Must be logged in"
        return render(request,"auctions/watchlist.html",{
            "message": message
        })

def removeFromWatchlist(request,listing_id):
    if request.user.is_authenticated:
        listing = Listing.objects.get(pk=listing_id)
        Watchlist = watchlist.objects.get(user = request.user)
        Watchlist.listings.remove(listing)
        Watchlist.save()
        listings = Watchlist.listings.all() # not .objects.all()
        return render(request,"auctions/watchlist.html",{
            "listings": listings
        })

    else:
        message = "Must be logged in"
        return render(request,"auctions/watchlist.html",{
            "message": message
        })
def comment(request, listing_id):
    #if the user is logged in
    currentListing = Listing.objects.get(pk=listing_id)
    if request.user.is_authenticated:
        #if the user is posting
        if request.method == 'POST':
            commentform = commentsForm(request.POST)
            if commentform.is_valid():
                commentMade = comments(
                    Comment= commentform.cleaned_data['Comment'],
                    user = request.user,
                    listing = currentListing #as soon as we said this as if i added this comment to the comments made about this listing and to get them use the related_name
                )
                commentMade.save()
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            else:
                #if form is invalid
                 bid_count=currentListing.bids.count()
                 return render(request,"auctions/listing.html",{
                    "listing":currentListing,
                    "bid_count": bid_count,
                    "commentForm":commentform
                    })

        else:
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        #else (the request is not post)
    #else (user not logged in)
    else:
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def categories(request):
    return render(request, "auctions/categories.html",{
        "Categories": Category.objects.all()
    })

def listsInCategory(request, category_id):
    categoryChosen = Category.objects.get(pk= category_id)
    return render(request, "auctions/index.html",{
        # First, use exclude to remove the inactive listings, then use filter to get the listings with the desired category.
        "listings":Listing.objects.exclude(active=False).filter(category=categoryChosen)
         #Listing.objects.exclude(active=False and category != categoryChosen) exclude with and don't work as expected
    })
"""
notes In Django, reverse is a function that generates a URL from a URL pattern name. In your code,
reverse("auctions:createListing") will generate the URL for the view that's named 'createListing' in the 'auctions' app.

When you use this inside HttpResponseRedirect, it means "redirect the user to the 'createListing' page".
This happens after the form data has been processed and everything is valid.


you
can i say watchlist = Watchlist.objects.get(user=request.user) if watchlist is not none: ...

ddb
Yes, you can use that line of code to get the current user's watchlist.
However, if the watchlist does not exist, the get method will raise a DoesNotExist exception, not return None.

you
now i got this AttributeError at /addToWatchlist/1
'ManyRelatedManager' object has no attribute 'objects'

ddb
The error message is indicating that you're trying to call .objects on a ManyRelatedManager object. This typically happens when you're trying to perform a query on a many-to-many field.

In your code, Watchlist.listings is a many-to-many field, so when you call Watchlist.listings.objects.all(), Django is trying to call .objects on Watchlist.listings, which is a ManyRelatedManager object, not a model.

To get all the listings in a watchlist, you can simply use Watchlist.listings.all(). The .all() method returns a QuerySet that represents all objects in the database for the many-to-many field.
"""


