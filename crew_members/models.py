from django.db import models


# Create your models here.
class CrewMember(models.Model):
    themoviedb_id = models.IntegerField()
    department = models.CharField(max_length=255)
    job = models.CharField(max_length=255)
    known_for_department = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    original_name = models.CharField(max_length=255)
    profile_path = models.CharField(max_length=255)
