from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.core import files
from django_extensions.db.fields import AutoSlugField
import time
import requests
from io import BytesIO
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.fields import ArrayField
from scripts.keygen import KeyGenerator

keygenenerator = KeyGenerator()

class Movie(models.Model):
	title = models.CharField(max_length=300)
	turkish_title = models.CharField(max_length=300)
	imdb_id = models.CharField(max_length=20, blank=True)
	listz_id = models.CharField(max_length=25, default=keygenenerator.generate_unique_key)
	year = models.CharField(max_length=25, blank=True)
	imdb_rating = models.CharField(max_length=10, blank=True)
	certificate = models.CharField(max_length=10, blank=True)
	runtime = models.CharField(max_length=25, blank=True)
	genres = models.ManyToManyField('Genre', blank=True)
	directors = models.ManyToManyField('Director', blank=True)
	actors = models.ManyToManyField('Actor', blank=True)
	stars = ArrayField(models.CharField(max_length=50), blank=True)
	countries = models.ManyToManyField('Country', blank=True)
	plot = models.TextField(max_length=500, blank=True)
	poster_url = models.URLField(blank=True, max_length=500)
	votes = models.CharField(max_length=12, blank=True)
	keywords = ArrayField(models.CharField(max_length=100), blank=True)
	slug = AutoSlugField(populate_from=['title', 'year'])
	vector_column = SearchVectorField(null=True)

	class Meta:
		indexes = [
			GinIndex(fields=['vector_column']),
		]

	def __str__(self):
		return self.title

	def avg_rating(self):
		if len(self.rating_set.all()) > 0:
			all_rates = self.rating_set.all().values_list('rate', flat=True)
			return sum(all_rates)/len(all_rates)

	def get_actors(self) -> str:
		cast = self.actors.all()
		cast_list = []
		for actor in cast:
			cast_list.append(actor.name)
		cast_list_string = ", ".join(cast_list[:3])
		return cast_list_string

	def get_directors(self) -> str:
		directors = self.directors.all()
		director_list = []
		for director in directors:
			director_list.append(director.name)
		director_list_string = ", ".join(director_list[:3])
		return director_list_string

	def get_genres(self) -> str:
		genres = self.genres.all()
		genre_list = []
		for genre in genres:
			genre_list.append(genre.name)
		genre_list_string = ", ".join(genre_list[:3])
		return genre_list_string

	def get_countries(self) -> str:
		countries = self.countries.all()
		country_list = []
		for	country in countries:
			country_list.append(country.name)
		country_list_string = ", ".join(country_list[:3])
		return country_list[0]

class Actor(models.Model):
	name = models.CharField(max_length=300, unique=True)
	slug = AutoSlugField(populate_from="name", null=True, max_length=300)
	movies = models.ManyToManyField('Movie', blank=True)

	def get_absolute_url(self):
		return reverse('actors', args=[self.slug])

	def __str__(self):
		return self.name 

class Director(models.Model):
	name = models.CharField(max_length=300)
	slug = AutoSlugField(populate_from="name", null=True, max_length=300)
	movies = models.ManyToManyField('Movie', blank=True)

	def get_absolute_url(self):
		return reverse('directors', args=[self.slug])
	
	def __str__(self):
		return self.name

class Genre(models.Model):
	name = models.CharField(max_length=70)
	slug = AutoSlugField(populate_from="name", null=True, max_length=300)
	movies = models.ManyToManyField('Movie', blank=True)

	def get_absolute_url(self):
		return reverse('genres', args=[self.slug])

	def __str__(self):
		return self.name

class Country(models.Model):
	name = models.CharField(max_length=300)
	slug = AutoSlugField(populate_from="name", null=True, max_length=300)
	movies = models.ManyToManyField('Movie', blank=True)

	def get_absolute_url(self):
		return reverse('countries', args=[self.slug])

	def __str__(self):
		return self.name

