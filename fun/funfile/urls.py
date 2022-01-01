
from django.urls import path, re_path

from . import views
from .apps import FunfileConfig

app_name = FunfileConfig.name

urlpatterns = [
    path('get_file/<str:file_id>', views.get_file, name='get_file'),
]
