from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from recommender.models import Movie
from django.contrib.auth.models import User
from django_extensions.db.fields import AutoSlugField
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from authz.models import Profile

class List(models.Model):
    CHOICES = (
        ('Common','Common'),
        ('Editor', 'Editor'),
        ('Personalized', 'Personalized'),
    )
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    movies = models.ManyToManyField(Movie, related_name="admin_lists", blank=True)
    type = models.CharField(max_length=50, choices=CHOICES)
    slug = AutoSlugField(populate_from=['title'], unique=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('list-to-grid-view', args=[str(self.slug)])

    def __str__(self):
        return self.title

    def get_movies(self):
        movies = self.movies.all()
        movie_list = []
        for movie in movies:
            movie_list.append(movie)
        return movie_list

class Watchlist(models.Model):
    title = models.CharField(max_length=40, blank=False)
    profile = models.ForeignKey(Profile, related_name="watchlists", on_delete=models.CASCADE)
    followers = models.ManyToManyField(Profile, related_name='following_watchlists', blank=True)
    movies = models.ManyToManyField(Movie, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    slug = AutoSlugField(populate_from=['user__username', 'title'], unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('list-to-grid-view', args=[str(self.slug)])

    def __str__(self):
        return str(self.title)

def max_movies_added(sender, **kwargs):
    if kwargs['instance'].movies.count() > 25:
        raise ValidationError('You can only assign 25 movies to a single watchlist.')

m2m_changed.connect(max_movies_added, sender=Watchlist.movies.through)