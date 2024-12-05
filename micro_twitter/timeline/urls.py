from django.urls import path

from micro_twitter.timeline import views

app_name = "timeline"

urlpatterns = [
    path(
        "tweets/",
        views.CreateTweetAPIView.as_view(),
        name="tweet-create",
    ),
    path(
        "home/",
        views.ListFollowingTweetsAPIView.as_view(),
        name="following-tweets-list",
    ),
]
