# Generated by Django 3.1.4 on 2021-01-21 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0009_auto_20210121_0255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genres',
            field=models.CharField(choices=[(0, 'Drama'), (1, 'Comedy')], max_length=100),
        ),
    ]
