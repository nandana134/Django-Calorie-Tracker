from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore

class Food(models.Model):
    name = models.CharField(max_length=100, unique=True)
    carbs = models.FloatField()
    protein = models.FloatField()
    fats = models.FloatField()
    calories = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.calories} kcal)"


class Consume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_consumed = models.ForeignKey(Food, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} consumed {self.food_consumed.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    calorie_goal = models.PositiveIntegerField(default=2000)

    def __str__(self):
        return f"{self.user.username}'s Profile"
