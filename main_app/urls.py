from django.urls import path
from . import views 

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.profile_index, name='profile-index'),
    path('profile/', views.profile, name='profile'),
    path('addProfile/', views.add_profile, name='add-profile'),
    path('foods/', views.food_list, name='food-list'),
    path('food/<int:pk>/', views.food_detail, name='food-detail'),
    path('foods/add-food/', views.add_food, name='add-food'),
    path('addMeal/', views.add_meal, name='add-meal'),
    path('meal/<int:pk>/edit/', views.meal_edit,   name='meal-edit'),
    path('meal/<int:pk>/delete/', views.meal_delete, name='meal-delete'),
    path('profile/<int:pk>/delete/', views.delete_profile, name='delete-profile'),


]