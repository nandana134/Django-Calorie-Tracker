import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from myapp.models import Food

class Command(BaseCommand):
    help = 'Import food data from food1.csv into the database'

    def handle(self, *args, **kwargs):
        # Construct the absolute path to the CSV file
        csv_file_path = os.path.join(settings.BASE_DIR,'myapp','food1.csv')

        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                count = 0
                for row in reader:
                    Food.objects.create(
                        name=row['food item'],
                        carbs=float(row['carbs']),
                        protein=float(row['protien']),  # Note: Typo in 'protien'
                        fats=float(row['fats']),
                        calories=int(row['calories'])
                    )
                    count += 1
                self.stdout.write(self.style.SUCCESS(f'Imported {count} food items successfully!'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
