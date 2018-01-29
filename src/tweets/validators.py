from django.core.exceptions import ValidationError


def validate_content(value):
    content = value
    if content == "":
        raise ValidationError("Content should be filled")
    elif content == 'abc':
        raise ValidationError("Content cannot be ABC")
    return value