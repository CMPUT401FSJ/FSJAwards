from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError(_("File must be in PDF format"))