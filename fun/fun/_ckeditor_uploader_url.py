from __future__ import absolute_import

from ckeditor_uploader import views
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.decorators.cache import never_cache

urlpatterns = [
    path('upload/', login_required(views.upload), name='ckeditor_upload'),
    path('browse/', never_cache(login_required(views.browse)),
         name='ckeditor_browse'),
]
