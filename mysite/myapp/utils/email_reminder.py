# myapp/utils/email_reminder.py

from django.core.mail import send_mail
from django.utils import timezone

def send_reminder_email(user):
    subject = "Calorie Tracker Reminder"
    message = f"Hi {user.username},\n\nDon't forget to log your meals today! Stay healthy and track your calories!"
    from_email = 'your_email@gmail.com'
    recipient_list = [user.email]
    
    send_mail(subject, message, from_email, recipient_list)
