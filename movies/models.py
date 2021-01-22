from datetime import timedelta, date
from django.utils.timezone import now
from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.


class Hall(models.Model):
    hallNum = models.IntegerField(primary_key=True)
    rows = models.PositiveSmallIntegerField(default=0)
    columns = models.PositiveSmallIntegerField(default=0)


class Movie(models.Model):
    name = models.CharField(blank=False, max_length=30)
    year = models.PositiveSmallIntegerField(default=0)
    duration = models.DurationField(default=timedelta())
    genres = models.CharField(blank=False, max_length=100)
    rate = models.DecimalField(decimal_places=1, max_digits=3, default=0, validators=(MinValueValidator(0), MaxValueValidator(10)))
    poster = models.URLField(default='')


class Screening(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, related_name='movie')
    hall = models.ForeignKey(Hall, on_delete=models.PROTECT, related_name='hall', null=True)
    screenDate = models.DateTimeField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99, validators=[MinValueValidator(0)])


class Ticket(models.Model):
    screening = models.ForeignKey(Screening, on_delete=models.PROTECT, null=True)
    row = models.PositiveSmallIntegerField(default=0)
    seat = models.PositiveSmallIntegerField(default=0)
    isTemp=models.BooleanField(default=True)
    user=models.SmallIntegerField(default=-1)