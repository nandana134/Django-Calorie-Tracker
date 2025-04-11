# myapp/management/commands/send_reminders.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import User
from myapp.models import Consume
from django.conf import settings

class Command(BaseCommand):
    help = 'Send daily reminder emails to users who haven’t logged food today'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()

        for user in User.objects.all():
            if not user.email:
                continue  # skip if no email

            has_logged_today = Consume.objects.filter(user=user, timestamp__date=today).exists()

            if not has_logged_today:
                subject = "👋 Friendly Reminder: Don't forget to log your meals!"
                message = f"Hi {user.username},\n\nYou haven’t logged any food today.\nKeep tracking your calories for better health!\n\n- Calorie Tracker"
                send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
