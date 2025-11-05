from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, Food,MealEntry


admin.site.register(Profile)
admin.site.register(Food)
admin.site.register(MealEntry)