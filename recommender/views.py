from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
import datetime
import tmdbv3api
import requests
import json
from recommender.models import Movie, Actor, Genre, Director, Country
from lists.models import List
from django.template.loader import render_to_string

# Create your views here.

API_KEY = "" #filled in private

tmdb = tmdbv3api.tmdb.TMDb()
tmdb.api_key = API_KEY

tmdbapi = tmdbv3api.Movie()
discover = tmdbv3api.Discover()
trending = tmdbv3api.Trending()
find = tmdbv3api.Find()
poster_path_url = "https://image.tmdb.org/t/p/w500"
person_path = "https://www.themoviedb.org/t/p/w300"

def find_person(person_id):
    results = find.find_by_imdb_id(person_id)
    for r in results['person_results']:
        print(f'{person_path}{r.profile_path}')

def get_release_year(year):
    year = [int(y) for y in year.split("-")]
    date = datetime.datetime(year[0],year[1],year[2])
    return date.strftime("%Y")

def get_movie(title):
    search = tmdbapi.search(title)
    return search

def get_movie_poster(search):
    poster = search[0].poster_path
    poster = str(poster_path_url) + str(poster)
    return poster

def home_page(request):
    
    no_country = Movie.objects.get(title="No Country for Old Men")
    w1917 = Movie.objects.get(title="1917")
    kill_bill = Movie.objects.get(title="Kill Bill: Vol. 1")
    movies = [kill_bill, w1917, no_country]
    context = {
        "no_country": no_country,
        "w1917": w1917,
        "kill_bill": kill_bill,
    }
    return render(request, "listz/homepage.html", context)

def recommender_page(request):
    lists = List.objects.all()
    context = {"lists": lists}
    return render(request, "listz/recommender_page/recommender.html", context)





