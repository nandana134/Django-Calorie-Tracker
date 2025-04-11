import csv
from django.core.management.base import BaseCommand # type: ignore
from myapp.models import Food

class Command(BaseCommand):
    help = 'Import food data from food1.csv into the database'

    def handle(self, *args, **kwargs):
        with open('food1.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                Food.objects.create(
                    name=row['food item'],
                    carbs=float(row['carbs']),
                    protein=float(row['protien']),
                    fats=float(row['fats']),
                    calories=int(row['calories'])
                )
                count += 1
            self.stdout.write(self.style.SUCCESS(f'Imported {count} food items successfully!'))
