from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex = r'^\+998\d{9}$',
    message = "Phone number must be in the format: '+998xxxxxxxxx'."
)