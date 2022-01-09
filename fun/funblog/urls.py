
from django.urls import path

from . import views


urlpatterns = [

    path('fblog_list', views.FblogListView.as_view(), name='fblog_list'),
    path('fblog_create/', views.FblogCreateView.as_view(),
         name='fblog_create'),
]