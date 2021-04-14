
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile_page, name="profile"),
    path("following", views.following_page, name="following"),
    
    #api route
    path("editPost/<int:post_id>", views.edit_post, name="editPost"),
    path("likePost/<int:post_id>", views.like_post, name="likePost"),
    path('loadLikes/<int:post_id>', views.load_likes, name="loadLikes")
]
