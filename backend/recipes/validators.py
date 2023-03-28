import re


from django.core.exceptions import ValidationError

PATTERN = r'^[-a-zA-Z0-9_]+$'


def slug_validator(value):
    incorrect = list(set(''.join(re.findall(PATTERN, value))))
    if incorrect:
        raise ValidationError(
            (f'можно использовать только буквы, цифры, -, _')
        )
    return value