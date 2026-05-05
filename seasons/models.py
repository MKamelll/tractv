from django.db import models
from shows.models import Show


# Create your models here.
class Season(models.Model):
    themoviedb_id = models.IntegerField()
    episode_count = models.IntegerField()
    name = models.CharField(max_length=255)
    overview = models.TextField(blank=True)
    poster_path = models.CharField()
    season_number = models.IntegerField()
    vote_average = models.FloatField()
    show = models.ForeignKey(to=Show, on_delete=models.CASCADE, related_name="seasons")
