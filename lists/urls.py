from django.urls import path
from . import views


urlpatterns = [
    path('lists/', views.lists, name="lists-main"),
    path('lists-by-editor/', views.lists_by_editor, name="lists-by-editor"),
    path('lists-from-public/', views.lists_from_public, name="lists-from-public"),
    path('lists-common/', views.lists_common, name="lists-common"),
    path('search/', views.search_movie, name="search-objects"),
    path('add_movie_to_list/', views.add_movie_to_list, name="add-movie-to-list"),
    path('lists/<slug:slug_text>/', views.lists_to_grid_view, name="list-to-grid-view"),
    path('ajax/grid_view_filter_data/<str:list_id>/', views.lists_grid_view_filter_data, name="grid-view-filter-data"),
    path('ajax/grid_view_filter/<str:list_id>/', views.lists_grid_view_filter, name="lists-grid-view-filter"),
    path('profile/create_watchlist/', views.create_watchlist, name="create-watchlist"),
    path('watched/<str:movie_id>/', views.add_to_watched, name="add-watched"),
    path('unwatched/<str:movie_id>/', views.remove_watched, name="remove-watched"),
    path('video/', views.watch_trailer, name="watch-trailer"),
    path('add_to_watchlist/<str:movie_id>/<str:watchlist_id>/', views.add_to_watchlist, name='add-to-watchlist'),
]