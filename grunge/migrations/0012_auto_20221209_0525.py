# Generated by Django 3.1.5 on 2022-12-09 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grunge', '0011_auto_20221209_0507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequencetrack',
            name='track_sequence',
            field=models.IntegerField(default=1),
        ),
    ]