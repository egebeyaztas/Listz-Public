# Generated by Django 3.1.7 on 2021-09-24 11:38

import authz.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recommender', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=40)),
                ('bio', models.TextField(blank=True, max_length=255)),
                ('profile_picture', models.ImageField(blank=True, default='', upload_to=authz.models.user_path)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('favourites', models.ManyToManyField(blank=True, related_name='faved_by', to='recommender.Movie')),
                ('is_watched', models.ManyToManyField(blank=True, related_name='watched_by', to='recommender.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=0)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommender.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authz.profile')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='rated_movies',
            field=models.ManyToManyField(blank=True, related_name='rated_users', through='authz.Rating', to='recommender.Movie'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]