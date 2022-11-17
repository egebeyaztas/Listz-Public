from django import forms
from django.forms.models import ModelMultipleChoiceField
from .models import List, Watchlist
from recommender.models import Movie

class MovieListCreationForm(forms.ModelForm):

    class Meta:
        model = List
        fields = ["title","movies","type"]

    title = forms.CharField()
    movies = ModelMultipleChoiceField(
        queryset=Movie.objects.filter(imdb_rating__gt=9.0),
    )

class SearchBarForm(forms.Form):
    q = forms.CharField(max_length=255)

class WatchlistCreationForm(forms.ModelForm):

    class Meta:
        model = Watchlist
        fields = ["title"]