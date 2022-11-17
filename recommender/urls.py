from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home'),
    path('recommender/', views.recommender_page, name="recommender_engine"),  
    #path('lists_sidebar_function/', views.ajax_request, name="ajax_request"),
]