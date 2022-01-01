
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog

from . import views

urlpatterns = [

    path('i18n/', include('django.conf.urls.i18n')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),

    path('homesticker_detail/<uuid:pk>',
         views.HomestickerDetailView.as_view(), name='homesticker_detail'),
    path('homesticker_list', views.HomestickerListView.as_view(),
         name='homesticker_list'),

    path('funhomesticker_detail/<uuid:pk>',
         views.FunhomestickerDetailView.as_view(),
         name='funhomesticker_detail'),
    path('funhomesticker_list', views.FunhomestickerListView.as_view(),
         name='funhomesticker_list'),

    path('appreciation_detail/<uuid:pk>',
         views.AppreciationDetailView.as_view(),
         name='appreciation_detail'),

    path('data_privacy', views.data_privacy, name='data_privacy'),
    path('legal_information', views.legal_information,
         name='legal_information'),

    path('favicon.ico', views.get_favicon_ico, name='favicon.ico'),

    path('#', views.HomeView.as_view(), name='##'),
    path('', views.HomeView.as_view(), name='#'),
]
