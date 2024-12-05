from django.urls import path

from micro_twitter.users import views

app_name = "users"

urlpatterns = [
    path("register/", views.RegisterUserAPIView.as_view(), name="user-register"),
    path(
        "login/",
        views.LoginUserAPIView.as_view(),
        name="user-login",
    ),
    path(
        "follow/",
        views.FollowUserAPIView.as_view(),
        name="user-follow",
    ),
]
