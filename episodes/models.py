from django.db import models
from shows.models import Show
from crew_members.models import CrewMember
from guest_stars.models import GuestStar


# Create your models here.
class Episode(models.Model):
    themoviedb_id = models.IntegerField()
    episode_type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    overview = models.TextField(blank=True)
    season_number = models.IntegerField()
    show = models.ForeignKey(to=Show, on_delete=models.CASCADE, related_name="episodes")
    still_path = models.CharField(max_length=255)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    crew = models.ManyToManyField(to=CrewMember, related_name="episodes")
    guests = models.ManyToManyField(to=GuestStar, related_name="episodes")
