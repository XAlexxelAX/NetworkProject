# Generated by Django 3.1.4 on 2021-01-20 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_auto_20210120_1829'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='movie_name',
        ),
        migrations.AddField(
            model_name='movie',
            name='name',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
