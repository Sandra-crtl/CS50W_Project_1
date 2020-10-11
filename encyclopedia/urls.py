from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.view_entry, name="view_entry"),
    path("add_entry", views.add_entry, name="add_entry"),
    path("edit_entry/<str:title>", views.edit_entry, name="edit_entry"),
    path("wiki/", views.random_entry, name="random_entry")
]
