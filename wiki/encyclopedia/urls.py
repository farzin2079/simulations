from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("search", views.search, name="search"),
    path("random_title", views.random_title, name="random_title"),
    path("wiki/delete/<str:title>", views.delete, name="delete"),
    path("wiki/<str:title>", views.entry, name="entry")
]
