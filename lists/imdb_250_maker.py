from lists.models import List
from recommender.models import Movie,Actor,Genre,Director,Country
import imdb

ia = imdb.IMDb()

search = ia.get_top250_movies()
movies_250 = []

for m in search:
    moviez = ia.get_movie(m.movieID)
    movies_250.append(moviez["localized title"])
    if not Movie.objects.filter(Turkish_title=moviez["localized title"]).exists():
        
        actor_obj, director_obj, country_obj, genre_obj = [],[],[],[]
        actor_db_obj, director_db_obj, country_db_obj, genre_db_obj = [],[],[],[]
        for actor in set(data[str(i)]["actors"]):
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
                genre_ = Genre.objects.get(title=genre)
                genre_db_obj.append(genre_)
            except:
                genre_ = Genre(title=genre)
                genre_obj.append(genre_)
        for country in set(data[str(i)]["country"]):
            try:
                country_ = Country.objects.get(name=country)
                country_db_obj.append(country_)
            except:
                country_ = Country(name=country)
                country_obj.append(country_)
        
        
        Genre.objects.bulk_create(genre_obj)
        Director.objects.bulk_create(director_obj)
        Actor.objects.bulk_create(actor_obj)
        Country.objects.bulk_create(country_obj)

        genre_db_obj += genre_obj
        director_db_obj += director_obj
        actor_db_obj += actor_obj
        country_db_obj += country_obj

        
        movie_ = Movie(
            Title=moviez["title"],
            Turkish_title=moviez["localized title"],
            Year=moviez["year"],
            Imdb_rating=moviez["rating"],
            Runtime=moviez["runtime"],
            Plot=moviez["plot inline"],
            Poster_url=moviez["full-size cover url"],
        )
        Movie.objects.bulk_create([movie_])    
        
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
        

        
        movie_.Genre.set(genre_db_obj)
        movie_.Actors.set(actor_db_obj)
        movie_.Director.set(director_db_obj)
        movie_.Country.set(country_db_obj)

#for i in range(5):
#    print(search[i]["localized title"])
#new_list = List.objects.create(title="Imdb 250", type="Common")

