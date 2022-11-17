import json
from recommender.models import Movie, Actor, Genre, Director, Country
from django.utils.text import slugify
import concurrent.futures
import time

with open("updated_database.json", "rb") as f:
    data = json.load(f)

counter = 1
movie_arr = []

start = time.time()
for i in range(103672):
    
    start_for_cats = time.time()
    actor_obj, director_obj, country_obj, genre_obj = [],[],[],[]
    actor_db_obj, director_db_obj, country_db_obj, genre_db_obj = [],[],[],[]
    for actor in set(data[str(i)]["cast"]):
        try:
            actor_ = Actor.objects.get(name=actor)
            actor_db_obj.append(actor_)
        except:
            actor_ = Actor(name=actor)
            actor_obj.append(actor_)
    for director in set(data[str(i)]["director"]):
        try:
            director_ = Director.objects.get(name=director)
            director_db_obj.append(director_)
        except:
            director_ = Director(name=director)
            director_obj.append(director_)
    for genre in set(data[str(i)]["genres"]):
        try:
            genre_ = Genre.objects.get(name=genre)
            genre_db_obj.append(genre_)
        except:
            genre_ = Genre(name=genre)
            genre_obj.append(genre_)
    for country in set(data[str(i)]["country"]):
        try:
            country_ = Country.objects.get(name=country)
            country_db_obj.append(country_)
        except:
            country_ = Country(name=country)
            country_obj.append(country_)
    end_for_cats = time.time() - start_for_cats
    
    Genre.objects.bulk_create(genre_obj)
    Director.objects.bulk_create(director_obj)
    Actor.objects.bulk_create(actor_obj)
    Country.objects.bulk_create(country_obj)

    genre_db_obj += genre_obj
    director_db_obj += director_obj
    actor_db_obj += actor_obj
    country_db_obj += country_obj

    start_for_movie_create = time.time()
    movie_ = Movie(
        title=data[str(i)]["title"],
        turkish_title=data[str(i)]["turkish_title"],
        imdb_id=data[str(i)]["imdb_id"],
        year=data[str(i)]["year"],
        imdb_rating=data[str(i)]["rating"],
        certificate=data[str(i)]["certificate"],
        runtime=data[str(i)]["runtime"],
        stars=data[str(i)]["stars"],
        plot=data[str(i)]["plot"],
        poster_url=data[str(i)]["poster_path"],
        votes=data[str(i)]["votes"],
        keywords=data[str(i)]["keywords"],

    )
    Movie.objects.bulk_create([movie_])    
    end_for_movie_create = time.time() - start_for_movie_create

    bulk_start = time.time()
    #Bulk Create m2m Connections
    ThroughModelGenre = Genre.movies.through
    ThroughModelDirector = Director.movies.through
    ThroughModelActor = Actor.movies.through
    ThroughModelCountry = Country.movies.through
    through_objs,through_objs2,through_objs3,through_objs4 = [],[],[],[]
    for genre in genre_db_obj:
        through_objs.append(
            ThroughModelGenre(
            movie_id = movie_.id,
            genre_id = genre.id
        ))
    for director in director_db_obj:
        through_objs2.append(
            ThroughModelDirector(
            movie_id = movie_.id,
            director_id = director.id
        ))
    for actor in actor_db_obj:
        through_objs3.append(
            ThroughModelActor(
            movie_id = movie_.id,
            actor_id = actor.id
        ))
    for country in country_db_obj:
        through_objs4.append(
            ThroughModelCountry(
            movie_id = movie_.id,
            country_id = country.id
        ))

    ThroughModelGenre.objects.bulk_create(through_objs)
    ThroughModelDirector.objects.bulk_create(through_objs2)
    ThroughModelActor.objects.bulk_create(through_objs3)
    ThroughModelCountry.objects.bulk_create(through_objs4)
    bulk_end = time.time() - bulk_start

    set_start = time.time()
    movie_.genres.set(genre_db_obj)
    movie_.actors.set(actor_db_obj)
    movie_.directors.set(director_db_obj)
    movie_.countries.set(country_db_obj)
    set_end = time.time() - set_start

    print(f'{counter}- Data migrated to the database successfully.')
    counter += 1

end = time.time() - start
print(f'Creating category objects time: {end_for_cats}')
print(f'Creating movie time: {end_for_movie_create}')
print(f'Creating bulk time: {bulk_end}')
print(f'Creating set time: {set_end}')
print(f'Script runtime: {end}')
    
'''
    #M2M Connections
    movie_.Genre.set(genre_obj)
    movie_.Actors.set(actor_obj)
    movie_.Director.set(director_obj)
    movie_.Country.set(country_obj)
    
    for actor in actor_obj:
        actor.movies.add(movie_)
        
    for director in director_obj:
        director.movies.add(movie_)
        
    for genre in genre_obj:
        genre.movies.add(movie_)
        
    for country in country_obj:
        country.movies.add(movie_)

    print(f'{counter}- Data migrated to the database successfully.')
    counter += 1
'''