from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
from decimal import *


def index(request):
    if request.user.id is not None:
        watchlist_count = Watchlist.objects.get(user=request.user).listing.count()
        return render(request, "auctions/index.html", {
            "all_listings": Listing.objects.filter(status=True).order_by('-time'),
            "watchlist_count": watchlist_count
        })
    else:
        return render(request, "auctions/index.html", {
            "all_listings": Listing.objects.filter(status=True).order_by('-time')
        } )

def all_listings(request):
    if request.user.id is not None:
        watchlist_count = Watchlist.objects.get(user=request.user).listing.count()
        return render(request, "auctions/listings.html", {
            "all_listings": Listing.objects.filter(status=True).order_by('-time'),
            "inactive": Listing.objects.filter(status=False),
            "watchlist_count": watchlist_count
        })
    else:
        return render(request, "auctions/listings.html", {
            "all_listings": Listing.objects.filter(status=True).order_by('-time'),
            "inactive": Listing.objects.filter(status=False),
        } )

def categories(request): 
    cat = dict(CATEGORIES)
    if request.user.id is not None:
        watchlist_count = Watchlist.objects.get(user=request.user).listing.count()
        return render(request, "auctions/categories.html", {
            "categories": cat,
            "watchlist_count": watchlist_count
            })
    else:
        return render(request, "auctions/categories.html", {
            "categories": cat
            })

def category_listing(request, category):
    listings = Listing.objects.filter(category=category.upper()).filter(status=True)
    if request.user.id is not None:
        watchlist_count = Watchlist.objects.get(user=request.user).listing.count()
        return render(request, "auctions/category_listing.html", {
            "category": category,
            "listings": listings,
            "watchlist_count": watchlist_count
        })
    else:
        return render(request, "auctions/category_listing.html", {
            "category": category,
            "listings": listings
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
            watchlist = Watchlist.objects.create(user=user)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == "POST":
        listing = ListingForm(request.POST)
       # try:
        new_listing = listing.save(commit=False)
        new_listing.seller = request.user
        if (new_listing.photo is None):
            new_listing.photo = "https://media.istockphoto.com/vectors/no-image-available-sign-vector-id922962354?k=6&m=922962354&s=612x612&w=0&h=_KKNzEwxMkutv-DtQ4f54yA5nc39Ojb_KPvoV__aHyU="
        new_listing.save()
        success = "Your listing has successfully been added"
        messages.success(request, success)
        return HttpResponseRedirect(reverse("index"))
        #except:
        #    error = "There was an error submitting this form - Try Again"
        #    return render(request, 'auctions/create.html', {
        #        "listing_form": listing,
       #         "error": error
       #     })
    else:       
        watchlist_count = Watchlist.objects.get(user=request.user).listing.count()
        return render(request, 'auctions/create.html', {
            "listing_form": ListingForm(),
            "watchlist_count": watchlist_count
        })


def make_bid(request, listing_pk):
    listingObj = Listing.objects.get(id=listing_pk)
    if (request.method == "POST" and request.user.id is not None):
        form = BidForm(request.POST)
        price = Decimal(request.POST.get('price'))
        highest_bid = listingObj.highest_bid
        print(highest_bid == None)
        if (highest_bid is not None and highest_bid.price.compare(price) == -1):
            if (form.is_valid):
                print("in bid not none")
                print(highest_bid.price)
                print(price)
                bid = form.save(commit=False)
                bid.user = request.user
                bid.listing = listingObj
                listingObj.highest_bid = bid
                bid.save()
                listingObj.save()
                message = "Your bid has successfully been placed. Thank you!"
                messages.success(request, message)
                return HttpResponseRedirect(reverse('listing', kwargs={'listing_pk': listing_pk}))
        elif (highest_bid is not None and highest_bid.price.compare(price) != -1):
            message = "Your bid must be greater than the current bid placed"
            messages.error(request, message) 
            return HttpResponseRedirect(reverse('listing', kwargs={'listing_pk': listing_pk}))  
        elif (highest_bid is None and price.compare(listingObj.price) == 1):
            if (form.is_valid):
                print("in bid none")
                bid = form.save(commit=False)
                bid.user = request.user
                bid.listing = listingObj
                listingObj.highest_bid = bid
                bid.save()
                listingObj.save()
            message = "Your bid has successfully been placed. Thank you!"
            messages.success(request, message)
            return HttpResponseRedirect(reverse('listing', kwargs={'listing_pk': listing_pk}))
        else:
            message = "Your bid must be greater than the starting price"
            messages.error(request, message) 
            return HttpResponseRedirect(reverse('listing', kwargs={'listing_pk': listing_pk}))  
    else:
        num_bids = Bid.objects.filter(listing=listing_pk).count()
        highest_bid = Bid.objects.filter(listing=listing_pk).order_by('price')
        comments = Comment.objects.filter(listing=listing_pk).order_by("-time").all()
        status = listingObj.status
        if (highest_bid.count() != 0):
            highest_bid = highest_bid.latest()
        else:
            highest_bid = None
        if (request.user.id is None):
            return render(request, "auctions/listing_bid.html", {
                "listing" : listingObj,
                "num_bids": num_bids,
                "highest_bid": highest_bid,
                "comments": comments,
                "status": status,
        })
        watchlist = Watchlist.objects.filter(user=request.user, listing=listing_pk).count()
        watchlist_count = Watchlist.objects.get(user=request.user).listing.count()
        watchlist_msg = ""
        if (watchlist == 0):
            watchlist_msg = "Add to Watchlist"
        else:
            watchlist_msg = "Remove from Watchlist"
        isWinner = False
        if (status == False and highest_bid is not None and listingObj.highest_bid.user == request.user):
            isWinner = True

        return render(request, "auctions/listing_bid.html", {
            "listing" : listingObj,
            "bid_form": BidForm(),
            "num_bids": num_bids,
            "highest_bid": highest_bid,
            "comments": comments,
            "comment_form": CommentForm(),
            "watchlist_msg": watchlist_msg,
            "status": status,
            "isWinner": isWinner,
            "watchlist_count": watchlist_count
        })

@login_required
def comment(request, listing_pk):
    listingObj = Listing.objects.get(id=listing_pk)
    if (request.method == "POST"):
        form = CommentForm(request.POST)
        if (form.is_valid):
            comment = form.save(commit=False)
            comment.user = request.user
            comment.listing = listingObj
            comment.save()
            return HttpResponseRedirect(reverse('listing', kwargs={'listing_pk': listing_pk}))

@login_required
def watchlist(request, listing_pk):
    if (request.method == "POST"):
        listingObj = Listing.objects.get(id=listing_pk)
        user_watchlist = Watchlist.objects.get(user=request.user)
        watchlist_item = Watchlist.objects.filter(user=request.user, listing=listing_pk)
        if (watchlist_item.count() == 0):
            #add
            user_watchlist.listing.add(listingObj)
            user_watchlist.save()
        else:
            #remove
            user_watchlist.listing.remove(listingObj)
            user_watchlist.save()

    return HttpResponseRedirect(reverse('listing', kwargs={'listing_pk': listing_pk}))

@login_required
def my_watchlist(request):
    if (request.method == "GET"):
        user_watchlist = Watchlist.objects.get(user=request.user)
        watchlist_count = Watchlist.objects.get(user=request.user).listing.count()
        return render(request, "auctions/watchlist.html", {
            "watchlist": user_watchlist.listing.order_by("-time").all(),
            "watchlist_count": watchlist_count
        })

@login_required
def close_bid(request, listing_pk):
    if (request.method == "POST"):
        listingObj = Listing.objects.get(id=listing_pk)  
        listingObj.status = False
        listingObj.save()
        
    return HttpResponseRedirect(reverse('listing', kwargs={'listing_pk': listing_pk}))