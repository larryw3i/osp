from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from django.utils.translation import gettext_lazy as _

from .models import Funuser


@admin.register(Funuser)
class FunuserAdmin(UserAdmin):
    pass
