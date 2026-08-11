from django.db import models
from django.contrib.auth.models import User
from api.models import Show, Episode


class Profile(models.Model):
    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE, related_name="profile"
    )
    name = models.CharField(max_length=256)
    favourite_quote = models.CharField(max_length=256)


class WatchStatus(models.Model):
    class Status(models.TextChoices):
        WATCHLIST = "watchlist", "Watchlist"
        WATCHING = "watching", "Watching"
        COMPLETED = "completed", "Completed"
        DROPPED = "dropped", "Dropped"

    profile = models.ForeignKey(
        to=Profile, on_delete=models.CASCADE, related_name="watch_statuses"
    )
    show = models.ForeignKey(
        to=Show, on_delete=models.CASCADE, related_name="watch_statuses"
    )
    status = models.CharField(max_length=20, choices=Status.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("profile", "show")


class EpisodeWatch(models.Model):
    profile = models.ForeignKey(
        to=Profile, on_delete=models.CASCADE, related_name="episode_watches"
    )
    episode = models.ForeignKey(
        to=Episode, on_delete=models.CASCADE, related_name="episode_watches"
    )
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("profile", "episode")


class ShowProgress(models.Model):
    profile = models.ForeignKey(
        to=Profile, on_delete=models.CASCADE, related_name="show_progress"
    )
    show = models.ForeignKey(
        to=Show, on_delete=models.CASCADE, related_name="show_progress"
    )
    episodes_watched = models.PositiveIntegerField(default=0)
    episodes_total = models.PositiveIntegerField(default=0)
    percent = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("profile", "show")
