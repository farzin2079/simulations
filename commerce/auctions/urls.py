from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("category/<str:category_id>", views.category, name="category" ),
    path("add_active", views.add_active, name="add_active"),
    path("add_category", views.add_category, name="add_category"),
    path("porpose/<str:active_id>", views.porpose, name="porpose"),
    path("<str:active_id>", views.active, name="active")
]
