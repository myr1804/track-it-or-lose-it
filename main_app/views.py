from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Food,MealEntry
from .forms import ProfileForm, MealEntryForm,FoodForm
from django.utils import timezone
from django.db.models import Sum, F

class Home(LoginView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html')
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to optional profile setup page
            return redirect('add-profile')
        else:
            error_message = 'Invalid signup - please try again'
    else:
        form = UserCreationForm()
        error_message = ''
    
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

def profile(request):
    return render(request, 'profile/profile.html')

def profile_index(request):
    today = timezone.now().date()
    qs = MealEntry.objects.filter(user=request.user, date=today, food__isnull=False).select_related('food')

    totals = qs.aggregate(
        total_calories=Sum(F('quantity') * F('food__calories')),
        total_proteins=Sum(F('quantity') * F('food__proteins')),
        total_carbs=    Sum(F('quantity') * F('food__carbs')),
        total_fats=     Sum(F('quantity') * F('food__fats')),
    )

    total_calories = totals.get('total_calories') or 0
    total_proteins = totals.get('total_proteins') or 0
    total_carbs    = totals.get('total_carbs')    or 0
    total_fats     = totals.get('total_fats')     or 0


    breakfast = qs.filter(meal_type='Breakfast')
    lunch     = qs.filter(meal_type='Lunch')
    dinner    = qs.filter(meal_type='Dinner')
    snack     = qs.filter(meal_type='Snack')

    context = {
        'breakfast_entries': breakfast,
        'lunch_entries':     lunch,
        'dinner_entries':    dinner,
        'snack_entries':     snack,
        'total_calories':    total_calories,
        'total_proteins':    total_proteins,
        'total_carbs':       total_carbs,
        'total_fats':        total_fats,
        'today': timezone.now().date(),
    }
    return render(request, 'profile/index.html', context)


def add_profile(request):
    profile = getattr(request.user, 'profile', None)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid() and any(profile_form.cleaned_data.values()):
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile-index')
    else:
        profile_form = ProfileForm(instance=profile)

    return render(request, 'profile/add_profile.html', {'profile_form': profile_form})

def delete_profile(request, pk):
    me = get_object_or_404(Profile, pk=pk, user=request.user)
    if request.method == 'POST':
        me.delete()
        return redirect('profile')



def food_list(request):
    query = request.GET.get('q', '').strip()
    if query:
        foods = Food.objects.filter(name__istartswith=query)
    else:
        foods = Food.objects.all()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        results = [{'id': food.id, 'name': food.name} for food in foods[:10]]
        return JsonResponse(results, safe=False)

    return render(request, 'food/food_list.html', {'foods': foods, 'query': query})

def food_detail(request, pk):
    food = get_object_or_404(Food, pk=pk)
    return render(request, 'food/food_detail.html', {'food': food})


def add_food(request):
    if request.method == 'POST':
        food_form = FoodForm(request.POST)
        if food_form.is_valid():
            food_form.save()
            return redirect('food-list')
    else:
        food_form = FoodForm()
    context = {
        'food_form': food_form,
    }
    return render(request, 'food/add_food.html', context)

def add_meal(request):
    meal_type_prefill = request.GET.get('meal_type', 'B')  

    if request.method == 'POST':
        form = MealEntryForm(request.POST)
        if form.is_valid():
            meal_entry = form.save(commit=False)
            meal_entry.user = request.user  
            meal_entry.date = timezone.now().date()  
            meal_entry.save()
            return redirect('profile-index') 
    else:
        form = MealEntryForm(initial={
            'meal_type': meal_type_prefill,
            'date': timezone.now().date(),
        })

    context = {'form': form}
    return render(request, 'food/add_meal.html', context)

def meal_edit(request, pk):
    me = get_object_or_404(MealEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MealEntryForm(request.POST, instance=me)
        if form.is_valid():
            form.save()
            return redirect('profile-index')
    else:
        form = MealEntryForm(instance=me)
    return render(request, 'food/edit_meal.html', {'form': form, 'meal':me})

def meal_delete(request, pk):
    me = get_object_or_404(MealEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        me.delete()
        return redirect('profile-index')