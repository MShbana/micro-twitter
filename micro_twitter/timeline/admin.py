from django.contrib import admin

from micro_twitter.timeline.models import Tweet


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    search_fields = [
        "author__email",
        "author__username",
        "public_id",
        "content",
    ]
    raw_id_fields = [
        "author",
    ]
    list_filter = [
        "time_created",
    ]
    list_display = [
        "public_id",
        "author",
        "content",
        "time_created",
    ]
    readonly_fields = [
        "public_id",
        "time_created",
    ]
