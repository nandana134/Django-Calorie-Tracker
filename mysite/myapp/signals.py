import sys
from django.db.models.signals import post_save, post_migrate  # type: ignore
from django.dispatch import receiver  # type: ignore
from django.contrib.auth.models import User  # type: ignore
from django.apps import apps
from django.core.management import call_command

from .models import UserProfile

# ---------------- UserProfile signal (existing) ----------------
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Maintain existing behavior: create a UserProfile on new User and attempt to save on every save.
    Tolerant to startup ordering; exceptions are caught and ignored.
    """
    if created:
        try:
            UserProfile.objects.create(user=instance)
        except Exception as e:
            # If the model/table isn't ready, skip creating now.
            print(f"[myapp] Could not create UserProfile for {instance}: {e}", file=sys.stderr)
            return
    try:
        instance.userprofile.save()
    except Exception:
        # If profile relation not available or saving fails during migrations, ignore.
        pass


# ---------------- post_migrate importer (calls existing management command) ----------------
@receiver(post_migrate)
def import_foods_after_migrate(sender, **kwargs):
    """
    After migrations finish, call the existing management command that imports food CSV.
    This reuses your existing import_food management command (command name 'import_food').
    It only runs when our app's migrations complete (sender.name == 'myapp') and avoids
    breaking the migrate operation by catching exceptions.
    """
    # Only run for our app to avoid calling multiple times for every app's migration.
    if sender.name != 'myapp':
        return

    # Ensure the Food model exists before calling the command.
    try:
        apps.get_model('myapp', 'Food')
    except LookupError:
        return

    # Call the management command. Use try/except to avoid breaking migrations.
    try:
        call_command('import_food')
        print("[myapp] Called import_food management command after migrate.")
    except Exception as e:
        # Don't fail migrations; log error for debugging.
        print(f"[myapp] import_food command failed: {e}", file=sys.stderr)
