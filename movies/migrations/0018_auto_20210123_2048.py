# Generated by Django 3.1.5 on 2021-01-23 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0017_movie_saleprice'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='salePrice',
            new_name='salePrec',
        ),
    ]
