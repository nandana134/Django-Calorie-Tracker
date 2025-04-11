from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from .models import Food, Consume, UserProfile
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.db.models import Sum, Count # type: ignore
from django.http import HttpResponse # type: ignore
from django.template.loader import get_template # type: ignore
from xhtml2pdf import pisa # type: ignore
from django.utils import timezone # type: ignore
from datetime import timedelta
from .forms import CalorieGoalForm
from .forms import CustomUserCreationForm
from collections import Counter


@login_required(login_url='login')
def index(request):
    query = request.GET.get('q')
    if query:
        foods = Food.objects.filter(name__icontains=query)
    else:
        foods = Food.objects.all()

    if request.method == "POST":
        food_consumed = request.POST.get('food_consumed')
        try:
            food = Food.objects.get(name=food_consumed)
            Consume.objects.create(user=request.user, food_consumed=food)
        except Food.DoesNotExist:
            messages.warning(request, "Food not found.")

    consumed_food = Consume.objects.filter(user=request.user).order_by('-timestamp')[:10]

    return render(request, 'myapp/index.html', {
        'foods': foods,
        'consumed_food': consumed_food,
        'query': query
    })


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})


@login_required(login_url='login')
def delete_consume(request, id):
    consumed_food = get_object_or_404(Consume, id=id, user=request.user)
    if request.method == 'POST':
        consumed_food.delete()
        return redirect('/')
    return render(request, 'myapp/delete.html', {'item': consumed_food})


@login_required(login_url='login')
def edit_consume(request, id):
    consumed_food = get_object_or_404(Consume, id=id, user=request.user)

    if request.method == 'POST':
        food_name = request.POST.get('food_consumed')
        try:
            new_food = Food.objects.get(name=food_name)
            consumed_food.food_consumed = new_food
            consumed_food.save()
            return redirect('index')
        except Food.DoesNotExist:
            messages.warning(request, "Food not found.")

    foods = Food.objects.all()
    return render(request, 'myapp/edit.html', {
        'item': consumed_food,
        'foods': foods,
        'selected food':consumed_food.food_consumed.name
    })


@login_required(login_url='login')
def daily_summary(request):
    today = timezone.now().date()
    consumed_today = Consume.objects.filter(user=request.user, timestamp__date=today)

    summary = consumed_today.aggregate(
        total_calories=Sum('food_consumed__calories'),
        total_protein=Sum('food_consumed__protein'),
        total_carbs=Sum('food_consumed__carbs'),
        total_fats=Sum('food_consumed__fats')
    )

    return render(request, 'myapp/summary.html', {
        'consumed_today': consumed_today,
        'summary': summary
    })


@login_required(login_url='login')
def user_profile(request):
    history = Consume.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'myapp/profile.html', {'history': history})

@login_required
def generate_report_pdf(request):
    user = request.user
    history = Consume.objects.filter(user=user).order_by('timestamp')
    total_days = history.values('timestamp__date').distinct().count()
    generated_on = timezone.now().strftime("%Y-%m-%d")

    total_calories = history.aggregate(Sum('food_consumed__calories'))['food_consumed__calories__sum'] or 0

    average_calories = round(total_calories / total_days, 2) if total_days > 0 else 0

    # Most frequent food
    food_names = [entry.food_consumed.name for entry in history]
    frequent_food = Counter(food_names).most_common(1)[0][0] if food_names else 'N/A'

    # Daily calorie totals
    from django.db.models.functions import TruncDate
    from django.db.models import F

    daily_totals = (
        history
        .annotate(day=TruncDate('timestamp'))
        .values('day')
        .annotate(total=Sum(F('food_consumed__calories')))
        .order_by('-total')
    )

    max_day = {
        'date': daily_totals[0]['day'] if daily_totals else 'N/A',
        'total': daily_totals[0]['total'] if daily_totals else 0
    }

    goal = getattr(user.userprofile, 'calorie_goal', None)

    days_under_goal = days_over_goal = 0
    if goal and daily_totals:
        for entry in daily_totals:
            if entry['total'] <= goal:
                days_under_goal += 1
            else:
                days_over_goal += 1

    goal_message = ""
    goal_message_type = ""
    if goal:
        if days_over_goal > days_under_goal:
            goal_message = "You've exceeded your calorie goal on most days. Consider making adjustments."
            goal_message_type = "warning"
        else:
            goal_message = "Great job staying within your calorie goal!"
            goal_message_type = "success"

    template = get_template('myapp/report_pdf.html')
    html = template.render({
        'user': user,
        'generated_on': generated_on,
        'goal': goal or 'Not Set',
        'report_duration': f"{total_days} day(s)",
        'total_days': total_days,
        'history': history,
        'total_calories': total_calories,
        'average_calories': average_calories,
        'max_day': max_day,
        'frequent_food': frequent_food,
        'days_under_goal': days_under_goal,
        'days_over_goal': days_over_goal,
        'goal_message': goal_message,
        'goal_message_type': goal_message_type,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="calorie_report.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response




@login_required(login_url='login')
def set_calorie_goal(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = CalorieGoalForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Calorie goal updated!")
            return redirect('summary')
    else:
        form = CalorieGoalForm(instance=profile)

    return render(request, 'myapp/set_goal.html', {'form': form})