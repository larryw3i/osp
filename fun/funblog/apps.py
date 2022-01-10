from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

app_name = 'funblog'
class FunblogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = app_name
    verbose_name = _('funblog')
