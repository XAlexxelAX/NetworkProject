# Generated by Django 3.1.4 on 2021-01-21 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0012_screening_relevant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='screening',
            name='relevant',
        ),
    ]
