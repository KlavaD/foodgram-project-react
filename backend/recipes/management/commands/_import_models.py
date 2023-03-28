import csv

from recipes.models import Ingredient


def import_ingredients():
    with open('data/ingredients.csv', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                data = Ingredient(
                    name=row[1],
                    measurement_unit=row[2])
                data.save()
        except Exception as error:
            raise ImportError(
                f'При импорте category.csv произошла ошибка {error}')
