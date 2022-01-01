
from django.urls import path

from . import views
from .apps import FunuserConfig

app_name = FunuserConfig.name

urlpatterns = [
    path('funuser_update/', views.FunuserUpdateView.as_view(),
         name='funuser_update'),
    path('funuser_detail/<int:user_id>',
         views.FunuserDetailView.as_view(), name='funuser_detail'),
]
