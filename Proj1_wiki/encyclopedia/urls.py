from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("random_entry", views.random_entry, name="random"),
    path("edit/<str:title>", views.edit, name="edit")
]
