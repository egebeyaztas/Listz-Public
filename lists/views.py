from authz.models import Profile
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
import tmdbv3api
import datetime
import requests
import json
import random
from recommender.models import Movie, Actor, Genre, Director, Country
from .models import List, Watchlist
from django.template.loader import render_to_string
from .forms import MovieListCreationForm, SearchBarForm, WatchlistCreationForm
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
API_KEY = "425abc217c220b8db4f189111e8e94d1"

tmdb = tmdbv3api.tmdb.TMDb()
tmdb.api_key = API_KEY

tmdbapi = tmdbv3api.Movie()
discover = tmdbv3api.Discover()
trending = tmdbv3api.Trending()
find = tmdbv3api.Find()
poster_path_url = "https://image.tmdb.org/t/p/w500"
person_path = "https://www.themoviedb.org/t/p/w300"

#main lists_page view
def lists(request):

    return render(request, "listz/lists_page/lists.html")

#lists_by_editor page views
@login_required(login_url='account_login')
def lists_by_editor(request):
    lists = List.objects.filter(type='Editor')

    context = {
        "lists": lists,
        }
        
    return render(request, "listz/lists_page/lists_carousel_view.html", context)

#lists public views
@login_required(login_url='account_login')
def lists_from_public(request):
    
    return render(request, 'listz/lists_page/lists_carousel_view.html')

# lists_common views
def lists_common(request):

        lists = List.objects.filter(type='Common')

        context = {
            "lists": lists,
            }
        
        return render(request, "listz/lists_page/lists_carousel_view.html", context)

def search_movie(request):
    form = SearchBarForm()

    if request.method == "GET":
            q = request.GET.get('Search', False)
            search_vectors = SearchVector('title', weight='A', config='english') + SearchVector('turkish_title', weight='B', config='turkish')
            search_query = SearchQuery(q, config='english') | SearchQuery(q, config='turkish')
            results = Movie.objects.annotate(search=search_vectors).filter(search=search_query).annotate(rank=SearchRank(search_vectors, search_query)).order_by('-imdb_rating')

            return render(request, 'listz/search.html', {'results': results})
    context = {
        'form': form,
            }

    return render(request, "listz/base.html", context)

def add_movie_to_list(request):
    if request.method == "POST":
        movie_id = request.POST.get('movie_to_list', False)
        movie = Movie.objects.get(id=movie_id)
        current_list = List.objects.get(id=3)
        current_list.movies.add(movie)
        print(f'{movie.title} added to the {current_list.title}')
        return redirect('home')

'''Grid View Functions'''
def get_person_path(person_id: str) -> str:
    results = find.find_by_imdb_id(person_id)
    person_paths = []
    for r in results["person_results"]:
        person_paths.append(person_path + r.profile_path)
    print(person_paths[0])
    return person_paths[0]

def lists_to_grid_view(request, slug_text: str):
    '''This function expands the chosen list to a grid view'''
    current_list = List.objects.get(slug=slug_text)
    movies = current_list.get_movies()
    random_trailer = watch_trailer()
    context = {
        'current_list': current_list,
        'movies': movies,
        'trailer': random_trailer
        }

    return render(request, 'listz/lists_page/lists_grid_view.html', context)

def lists_grid_view_filter_data(request, list_id: int):
    '''This function filters the grid view list with parameters:
        Genre, Cast, Country, Runtime, Rating, Director
    '''
    if request.is_ajax() and request.method == "GET":
        db_movies = List.objects.get(id=list_id).get_movies()
        
        db_genres = []
        db_countries = []
        db_cast = []
        db_director = []
        for movie in db_movies:
            db_genres += [m['name'] for m in movie.genres.all().values('name')]
            db_countries += [m['name'] for m in movie.countries.all().values('name')]
            db_cast += [m['name'] for m in movie.actors.all().values('name')]
            db_director += [m['name'] for m in movie.directors.all().values('name')]
        
        db_final_genres = list(set(db_genres))
        db_final_countries = list(set(db_countries))
        db_final_cast = list(set(db_cast))
        db_final_director = list(set(db_director))
        data = {
            "genres": db_final_genres,
            "countries": db_final_countries,
            "actors": db_final_cast,
            "directors": db_final_director,
        }

        return JsonResponse(data)

def lists_grid_view_filter(request, list_id: int):
    ''' Main Filter Function '''
    if request.is_ajax() and request.method == "POST":
        current_list = List.objects.get(id=list_id)
        filters = {}
        
        for key in request.POST.dict().keys():
            if key != 'csrfmiddlewaretoken':
                filters[f'{key[:-2]}__name__in'] = request.POST.getlist(key)
            else:
                continue
        print(filters)
        movies_filtered = current_list.movies.all().filter(**filters).distinct()
        
        context = {
            "current_list": current_list,
            "movies": movies_filtered,
            "user": request.user,
        }
        html = render_to_string('listz/lists_page/grid_view_template.html', context)        
        return JsonResponse(html, safe=False)

'''Create Watchlist'''
@login_required(login_url="account_login")
def create_watchlist(request):
    form = WatchlistCreationForm()

    if request.method == "POST" and request.is_ajax():
        
        form = WatchlistCreationForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            watchlist = Watchlist(user=request.user ,title=title)
            watchlist.save()
            return JsonResponse({'succesful': 'Watchlist succesfully created.'}, safe= False)
    
    context = {
        "form": form,
    }

    return render(request, 'listz/profile/create_watchlist.html', context)

@login_required(login_url="account_login")
def add_to_watched(request, movie_id):
    if request.method == "POST" and request.is_ajax():
        watched=False
        print(request.user.id)
        movie = Movie.objects.get(id=movie_id)
        profile = Profile.objects.get(user__id=request.user.id)
        if movie in profile.is_watched.all():
            raise Exception('Already watched.')
        else:
            profile.movie_is_watched(movie)
            watched=True
            context = {
                'added': f'{movie.title} watched.',
                'watched': watched,
            }
            return JsonResponse(context, safe=False)

@login_required(login_url="account_login")
def remove_watched(request, movie_id):
    if request.method == "POST" and request.is_ajax():
        watched=True
        print(request.user.id)
        movie = Movie.objects.get(id=movie_id)
        profile = Profile.objects.get(user__id=request.user.id)
        if not movie in profile.is_watched.all():
            raise Exception('Not watched.')
        else:
            profile.movie_unwatched(movie)
            watched=False
            context = {
                'added': f'{movie.title} unwatched.',
                'watched': watched,
            }
            return JsonResponse(context, safe=False)

def watch_trailer():
    res = find.find_by_imdb_id('tt2382320')
    for r in res['movie_results']:
        tmdb_movie_id = r.id
    
    base = "https://api.themoviedb.org/3/movie/"
    url = base + str(tmdb_movie_id) + '/videos?api_key=' + API_KEY + '&language=en-US'
    response = requests.get(url).json()
    #print(response)
    trailer_urls = []
    for trailer in response['results']:
        if trailer['type'] == 'Trailer':
            trailer_url = 'https://www.youtube.com/embed/' + trailer['key'] + '?playsinline=1'
            trailer_urls.append(trailer_url)
    try:
        random_trailer = random.choice(trailer_urls)
    except:
        pass
    #print(trailer_urls)

    context = {
        'trailer': random_trailer,
    }

    return random_trailer

def add_to_watchlist(request, movie_id, watchlist_id):
    if request.method == 'POST' and request.is_ajax():
        movie = Movie.objects.get(id=movie_id)
        watchlist = request.user.watchlist_owner.get(id=watchlist_id)
        if movie in watchlist.movies.all():
            raise Exception('already in watchlist.')
        else:
            watchlist.movies.add(movie)
            watchlist.save()

        return JsonResponse({'movie': movie.title, 'added': f'added to the {watchlist.title}'})
        