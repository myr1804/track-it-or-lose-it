from django import forms
from .models import Food, Profile, MealEntry

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'gender', 'age','height', 'weight']
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'gender': 'Gender',
            'age': 'Age (years)',
            'height': 'Height (in)',
            'weight': 'Weight (lb)',
        }

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'calories', 'proteins', 'carbs', 'fats']
        labels = {
            'name': 'Food Name',
            'calories': 'Calories',
            'proteins': 'Proteins (g)',
            'carbs': 'Carbohydrates (g)',
            'fats': 'Fats (g)',
        }


class MealEntryForm(forms.ModelForm):
    class Meta:
        model = MealEntry
        fields = ['meal_type', 'date', 'food', 'quantity']
        labels = {
            'meal_type': 'Meal Type',
            'date': 'Date',
            'food': 'Food',
            'quantity': 'Quantity',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'meal_type': forms.Select(attrs={'style': 'width: 100%; padding: 5px;'}),
            'food': forms.Select(attrs={'style': 'width: 100%; padding: 5px;'}),
            'quantity': forms.NumberInput(attrs={'style': 'width: 100%; padding: 5px;'}),
        }