from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from micro_twitter.timeline.models import Tweet

User = get_user_model()


class TweetAPITests(TestCase):

    def setUp(self):
        # Create test users.
        self.user1 = User.objects.create_user(
            email="user1@gmail.com", password="password"
        )
        self.user2 = User.objects.create_user(
            email="user2@gmail.com", password="password"
        )
        self.user3 = User.objects.create_user(
            email="user3@gmail.com", password="password"
        )

        # Create tweets.
        self.tweet1 = Tweet.objects.create(
            author=self.user1, content="Tweet from user1"
        )
        self.tweet2 = Tweet.objects.create(
            author=self.user2, content="Tweet from user2"
        )
        self.tweet3 = Tweet.objects.create(
            author=self.user3, content="Tweet from user3"
        )

        # User1 follows user2 (so user1 should see user2's tweets).
        self.user1.following.add(self.user2)

        # Set up APIClient.
        self.client = APIClient()

    def test_create_tweet(self):
        """Test the creation of a tweet."""
        self.client.force_authenticate(user=self.user1)
        data = {"content": "New tweet from user1"}
        url = reverse("timeline:tweet-create")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tweet.objects.count(), 4)
        self.assertEqual(Tweet.objects.last().author, self.user1)

    def test_list_following_tweets(self):
        """Test that ListFollowingTweetsAPIView only returns tweets from followed users."""
        url = reverse("timeline:following-tweets-list")
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # The response should contain tweets from user2 only, as user1 follows user2.
        tweets = [tweet["content"] for tweet in response.data["results"]]
        self.assertIn("Tweet from user2", tweets)
        self.assertNotIn("Tweet from user1", tweets)
        self.assertNotIn("Tweet from user3", tweets)

    def test_list_following_tweets_pagination(self):
        """Test that pagination works correctly in ListFollowingTweetsAPIView."""
        # Add 20 more tweets for user2 to test pagination.
        for i in range(20):
            Tweet.objects.create(author=self.user2, content=f"Tweet {i + 4} from user2")

        url = reverse("timeline:following-tweets-list")
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # The response should be paginated and should return a 'next' link.
        self.assertIn("next", response.data)
        self.assertEqual(len(response.data["results"]), 5)
