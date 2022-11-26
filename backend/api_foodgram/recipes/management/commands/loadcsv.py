import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Create model objects from CSV file'

    def add_argument(self):
        pass

    def handle(self, *args, **options):
        with open('ingredients.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
