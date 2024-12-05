from rest_framework.generics import CreateAPIView, ListAPIView

from micro_twitter.common.pagintaion import SmallResultsSetLimitOffsetPagination
from micro_twitter.timeline.models import Tweet
from micro_twitter.timeline.serializers import TweetSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import status


@extend_schema(
    summary="Create a new tweet.",
    description="Endpoint to create a new tweet by the authenticated user.",
    request=TweetSerializer,
    responses={status.HTTP_200_OK: TweetSerializer},
)
class CreateTweetAPIView(CreateAPIView):
    serializer_class = TweetSerializer

    def perform_create(self, serializer) -> None:
        serializer.save(author=self.request.user)


@extend_schema(
    summary="List tweets by following accounts.",
    description=(
        "Endpoint to retrieve a list of all tweets created by"
        " the accounts followed by the authenticated user."
    ),
    responses={status.HTTP_200_OK: TweetSerializer(many=True)},
)
class ListFollowingTweetsAPIView(ListAPIView):
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()
    pagination_class = SmallResultsSetLimitOffsetPagination

    def get_queryset(self):
        return super().get_queryset().filter(
            author__followed_by=self.request.user,
        ).order_by(
            "-time_created",
        )
