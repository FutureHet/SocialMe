# Generated by Django 3.2.9 on 2021-11-11 17:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0007_song_upload_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='plan',
            field=models.CharField(default='free', max_length=10),
        ),
        migrations.AlterField(
            model_name='song',
            name='upload_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 11, 23, 1, 10, 243313)),
        ),
    ]
