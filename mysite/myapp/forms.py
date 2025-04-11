from django import forms # type: ignore
from .models import Food
from django.contrib.auth.forms import UserCreationForm # type: ignore
from django.contrib.auth.models import User # type: ignore
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class FoodSelectForm(forms.Form):
    food = forms.ModelChoiceField(queryset=Food.objects.all(), label="Select Food")

class CalorieGoalForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['calorie_goal']