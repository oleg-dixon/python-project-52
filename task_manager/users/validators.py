from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

username_validator = RegexValidator(
    regex=r'^[\w.@+-]+\Z',
    message=_('Только буквы, цифры и символы @/./+/-/_.')
)