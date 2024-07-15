from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

def validate_sa_id_number(value):
    id_number = str(value).strip()

    # Check if the ID number is 13 digits long
    if len(id_number) != 13:
        raise ValidationError(_('South African ID number must be exactly 13 digits long.'), code='invalid')

    # Check if all characters are digits
    if not id_number.isdigit():
        raise ValidationError(_('South African ID number must only contain digits.'), code='invalid')

    # Luhn algorithm validation
    #check_digit = int(id_number[-1])
    #partial_id = id_number[:12]
    #sum_value = sum(int(partial_id[i]) * (2 if i % 2 == 0 else 1) for i in range(12))
    #calculated_check_digit = (10 - (sum_value % 10)) % 10

    #if check_digit != calculated_check_digit:
        #raise ValidationError(_('Invalid South African ID number.'), code='invalid')
