from django.db import models


# Create your models here.
class GuestStar(models.Model):
    themoviedb_id = models.IntegerField()
    character = models.CharField(max_length=255)
    known_for_department = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    original_name = models.CharField(max_length=255)
    profile_path = models.CharField(max_length=255)
