from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:listing_pk>", views.make_bid, name="listing"),
    path("comment/<int:listing_pk>", views.comment, name="comment"),
    path("watchlist/<int:listing_pk>", views.watchlist, name="watchlist"),
    path("my_watchlist", views.my_watchlist, name="my_watchlist"),
    path("close_bid/<int:listing_pk>", views.close_bid, name="close_bid"),
    path("all_listings", views.all_listings, name="all"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category_listing, name="category_listing")
]
