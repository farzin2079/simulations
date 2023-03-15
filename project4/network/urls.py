
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    path("following", views.following, name="following"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("like/<int:post_id>", views.like, name="like"),
    path("addpost", views.addpost, name='addpost'),
    path("edit/<int:post_id>", views.edit, name='edit'),
    path("delete/<int:post_id>", views.delete, name='delete'),
    path("profile/<int:user_id>", views.profile, name="profile"),
]
