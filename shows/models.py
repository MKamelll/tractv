from django.db import models


# Create your models here.
class Show(models.Model):
    themoviedb_id = models.IntegerField()
    name = models.CharField(max_length=255)
    number_of_episodes = models.IntegerField()
    number_of_seasons = models.IntegerField()
    origin_country = models.CharField(max_length=255)
    original_language = models.CharField(max_length=255)
    original_name = models.CharField(max_length=255)
    overview = models.TextField(blank=True)
    poster_path = models.CharField(max_length=255)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
