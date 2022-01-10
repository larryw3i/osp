
from django.urls import path

from . import views
from .apps import app_name

app_name = app_name

urlpatterns = [

    path('', views.FblogListView.as_view(), name='list'),
    path('create/', views.FblogCreateView.as_view(),
         name='create'),
]
