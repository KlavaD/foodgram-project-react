from django.core.management.base import BaseCommand, CommandError

from recipes.management.commands._import_models import import_ingredients, \
    create_tags


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            create_tags()
            import_ingredients()
        except Exception as error:
            raise CommandError(f'Сбой при импорте: {error}')

        self.stdout.write(self.style.SUCCESS('Импорт прошел успешно'))
