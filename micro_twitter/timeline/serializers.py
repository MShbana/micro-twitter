from rest_framework import serializers

from micro_twitter.timeline.models import Tweet
from micro_twitter.users import serializers as users_serializers


class TweetSerializer(serializers.ModelSerializer):
    author = users_serializers.UserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = [
            "public_id",
            "content",
            "time_created",
            "author",
        ]
        extra_kwargs = {
            "public_id": {
                "read_only": True,
            },
            "time_created": {
                "read_only": True,
            },
        }
