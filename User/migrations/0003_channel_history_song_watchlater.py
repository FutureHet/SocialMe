# Generated by Django 3.2.8 on 2021-10-26 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_usermodel_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('channel_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1000)),
                ('music', models.CharField(max_length=100000000)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('song_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=2000)),
                ('singer', models.CharField(max_length=2000)),
                ('tags', models.CharField(max_length=100)),
                ('image', models.CharField(default='', max_length=100000)),
                ('song', models.FileField(upload_to='images')),
                ('movie', models.CharField(default='', max_length=1000)),
                ('credit', models.CharField(default='', max_length=100000)),
            ],
        ),
        migrations.CreateModel(
            name='Watchlater',
            fields=[
                ('watch_id', models.AutoField(primary_key=True, serialize=False)),
                ('video_id', models.CharField(default='', max_length=10000000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('hist_id', models.AutoField(primary_key=True, serialize=False)),
                ('music_id', models.CharField(default='', max_length=10000000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.usermodel')),
            ],
        ),
    ]