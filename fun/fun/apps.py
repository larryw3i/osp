from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FunConfig(AppConfig):
    name = 'fun'
    verbose_name = _('Fun')
