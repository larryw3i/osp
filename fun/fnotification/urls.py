
from django.urls import path

from . import views
from .apps import app_name

app_name = app_name


urlpatterns = [
    path('list', views.FnotificationListView.as_view(), name='list'),
]
