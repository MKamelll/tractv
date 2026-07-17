from django.db import models


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


class Season(models.Model):
    themoviedb_id = models.IntegerField()
    episode_count = models.IntegerField()
    name = models.CharField(max_length=255)
    overview = models.TextField(blank=True)
    poster_path = models.CharField()
    season_number = models.IntegerField()
    vote_average = models.FloatField()
    show = models.ForeignKey(to=Show, on_delete=models.CASCADE, related_name="seasons")


class CrewMember(models.Model):
    themoviedb_id = models.IntegerField()
    department = models.CharField(max_length=255)
    job = models.CharField(max_length=255)
    known_for_department = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    original_name = models.CharField(max_length=255)
    profile_path = models.CharField(max_length=255)


class GuestStar(models.Model):
    themoviedb_id = models.IntegerField()
    character = models.CharField(max_length=255)
    known_for_department = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    original_name = models.CharField(max_length=255)
    profile_path = models.CharField(max_length=255)


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
