from datetime import timedelta
from django.db import models

class Hall(models.Model):
    hallNum = models.IntegerField()


class Movie(models.Model):
    movieid = models.CharField(max_length=10, primary_key=True)
    moviename = models.CharField(max_length=30)
    year = models.IntegerField(default=0)
    duration = models.DurationField(default=timedelta())
    genres = models.CharField(max_length=100)
    rate = models.IntegerField(default=0)
    poster = models.URLField(default='')

class Screening(Movie):
    screenDate = models.DateTimeField()
    price = models.IntegerField()
    hall = Hall()

class Ticket(models.Model):
    screening = Screening()
