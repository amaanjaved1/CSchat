
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:page_id>", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add, name="add"),
    path("following/<int:page_id>", views.following, name="following"),
    path("profile/<int:user_id>", views.profile, name="profile"),

    #API routes 
    path("likes/<int:post_id>", views.likes, name="likes"),
    path("follow/<int:profile_id>", views.follow, name="follow"),
    path("edit/<int:post_id>", views.edit, name="edit")
]
