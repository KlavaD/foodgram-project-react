import csv

from recipes.models import Ingredient


def import_ingredients():
    with open('data/ingredients.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        id = 0
        try:
            for name, m_unit in reader:
                data, status = Ingredient.objects.get_or_create(
                    name=name,
                    measurement_unit=m_unit)
                id += status
                if id % 100 == 0:
                    print('ингредиенты загружаются, ждите')

        except Exception as error:
            raise ImportError(
                f'При импорте произошла ошибка {error}')

# def create_tags():
#     tags={
#
#     }
#         try:
#             for name, m_unit in reader:
#                 data, status = Ingredient.objects.get_or_create(
#                     name=name,
#                     measurement_unit=m_unit)
#                 id += status
#                 if id % 100 == 0:
#                     print('ингредиенты загружаются, ждите')
#
#         except Exception as error:
#             raise ImportError(
#                 f'При импорте произошла ошибка {error}')