# Generated by Django 3.1.5 on 2021-01-22 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0013_remove_screening_relevant'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='isTemp',
            field=models.BooleanField(default=True),
        ),
    ]