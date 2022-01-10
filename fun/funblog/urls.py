
from django.urls import path

from . import views


urlpatterns = [

    path('list', views.FblogListView.as_view(), name='fblog_list'),
    path('create/', views.FblogCreateView.as_view(),
         name='create'),
]