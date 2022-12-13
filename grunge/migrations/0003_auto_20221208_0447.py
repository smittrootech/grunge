# Generated by Django 3.1.5 on 2022-12-08 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grunge', '0002_playlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='tracks',
            field=models.ManyToManyField(related_name='tracks_in_playlist', to='grunge.Track'),
        ),
    ]
