from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

app_name = 'eduhub'


class EduhubConfig(AppConfig):
    name = app_name
    verbose_name = _('Eduhub')
