# Generated by Django 3.2.8 on 2021-10-26 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0004_alter_usermodel_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='profile_image',
            field=models.ImageField(blank=True, default='https://www.gravatar.com/avatar/00000000000000000000000000000000?d=https%3A%2F%2Fexample.com%2Fimages%2Favatar.jpg', upload_to='images/%Y/%m/%d/'),
        ),
    ]
