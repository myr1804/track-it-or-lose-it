from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django import forms

class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
         return f"{self.user.username}'s Profile"
    

class Food(models.Model):
    name = models.CharField(max_length=100)
    calories = models.FloatField()
    proteins = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()

    def __str__(self):
         return self.name
    


class MealEntry(models.Model):
    MEAL_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True, blank=True)
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)
    quantity = models.FloatField(default=1)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.meal_type} - {self.food}"