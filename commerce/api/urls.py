from django.urls import path
from . import views


urlpatterns = [
    path('', views.getRoute),
    path('listings', views.getListings),
    path('listings/<str:id>', views.getListing)
]
