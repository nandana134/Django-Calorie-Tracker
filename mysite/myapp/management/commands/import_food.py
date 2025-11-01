import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from myapp.models import Food

class Command(BaseCommand):
    help = 'Import food data from myapp/food1.csv into the database (idempotent)'

    def handle(self, *args, **kwargs):
        # Construct the absolute path to the CSV file placed inside the app directory
        csv_file_path = os.path.join(settings.BASE_DIR, 'myapp', 'food1.csv')

        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file_path}'))
            return

        count_created = 0
        count_skipped = 0
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Tolerant column handling and trimming
                name = (row.get('food item') or row.get('name') or '').strip()
                if not name:
                    count_skipped += 1
                    continue

                # Avoid duplicates (case-insensitive)
                if Food.objects.filter(name__iexact=name).exists():
                    count_skipped += 1
                    continue

                carbs = row.get('carbs') or row.get('carbohydrates') or '0'
                # tolerate typo 'protien' and proper 'protein'
                protein = row.get('protien') or row.get('protein') or '0'
                fats = row.get('fats') or '0'
                calories = row.get('calories') or '0'

                try:
                    Food.objects.create(
                        name=name,
                        carbs=float(carbs or 0),
                        protein=float(protein or 0),
                        fats=float(fats or 0),
                        calories=int(float(calories or 0))
                    )
                    count_created += 1
                except Exception as e:
                    # Skip bad rows, but log them to stdout for debugging
                    self.stdout.write(self.style.WARNING(f"Skipping row for '{name}': {e}"))
                    count_skipped += 1
                    continue

        self.stdout.write(self.style.SUCCESS(
            f'Imported {count_created} food items successfully. Skipped {count_skipped} rows.'
        ))
