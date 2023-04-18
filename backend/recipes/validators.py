from django.core.exceptions import ValidationError


def positive_validator(value):
    if value < 1:
        raise ValidationError(
            (f'Время приготовления должно быть больше 1')
        )
    return value
