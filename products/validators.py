from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def my_blank_validator(value):
    if not value == None:
        raise ValidationError("Sorry, My Blank Validator ERROR!", status='invalid')

