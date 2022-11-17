from django.urls import path
from authz import views
urlpatterns = [
    path('welcome/', views.welcome_page, name="welcome"),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin-dashboard'),
    path('editor-dashboard/', views.editor_dashboard_view, name='editor-dashboard'),
    path('user/<str:user_name>/', views.user_profile, name='profile'),
    path('profile/update-profile/', views.update_profile, name='edit-profile'),
    path('profile/get_watchlists_for_profile', views.get_watchlists_for_profile, name='get-watchlists-for-profile'),
]