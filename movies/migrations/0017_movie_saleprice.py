# Generated by Django 3.1.5 on 2021-01-23 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0016_movie_agelimit'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='salePrice',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
