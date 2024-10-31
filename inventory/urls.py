from django.urls import path
from . import views

urlpatterns = [
    path("", views.Controlroom, name="inventory"),
    path("<int:item_id>/", views.Itemdetails, name="Item Details")
]
