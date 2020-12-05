from main.views import add_ingredient
from django.urls import path, include
from . import views



app_name = 'UsersAuth'

urlpatterns = [
    path('', include('main.urls')),
    path('login/', views.loginview, name = 'login'),
    path('logout/', views.logoutview, name = 'logout'),
    path('register/',views.register, name = 'register'),
    path('<int:user_id>/profile/',views.profile_view, name = 'profile'),
    
    ]
