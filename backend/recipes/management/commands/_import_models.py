import csv

from recipes.models import Ingredient


def import_ingredients():
    with open('data/ingredients.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        id = 0
        try:
            for row in reader:
                data = Ingredient(id=id,
                                  name=row[0],
                                  measurement_unit=row[1])
                id += 1
                data.save()
        except Exception as error:
            raise ImportError(
                f'При импорте произошла ошибка {error}')
