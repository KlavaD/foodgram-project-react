import csv

from recipes.models import Ingredient, Tag


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


tags = (
    ('завтрак', 'breakfast', '#c9eb34'),
    ('обед', 'lunch', '#c034eb'),
    ('ужин', 'dinner', '#ebd334'),
    ('десерт', 'desert', '#34dceb'),
)
result = []


def create_tags():
    global result, tags
    try:
        with open('data/tags.csv', encoding='utf-8') as csvfile:
            reader_obj = csv.reader(csvfile)
            for tag in reader_obj:
                result.append(tag)
    except Exception as error:
        print(f'Ошибка {error}')
    try:
        if result:
            tags = result
        for name, slug, color in tags:
            data, status = Tag.objects.get_or_create(
                name=name,
                slug=slug,
                color=color
            )
        print('Тэги созданы!')
    except Exception as error:
        raise ImportError(
            f'При импорте произошла ошибка {error}')
