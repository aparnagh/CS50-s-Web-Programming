from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import PROTECT
from django.db.models.fields import related


CATEGORIES = (
    ("HOME", "Home"),
    ("TECH", "Technology"),
    ("BOOKS", "Books"),
    ("BEAUTY", "Beauty"),
    ("HEALTH", "Health"),
    ("FASHION", "Fashion"),
    ("STATIONARY", "Stationary"),
    ("OTHER", "Other"),
    )

class User(AbstractUser):
    pass

    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_bids")
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'price'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_comments")
    comment = models.CharField(max_length=2000)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name="comments")
    time = models.DateTimeField(auto_now_add=True)

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=350, blank=True, null=True)
    photo = models.CharField(max_length=2048, blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    highest_bid = models.ForeignKey(Bid, related_name="highest_bid", null=True, blank=True, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    category = models.CharField(max_length=10, blank=True, choices=CATEGORIES, default="OTHER")
    time = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_watchlist")
    listing = models.ManyToManyField(Listing, null=True)

