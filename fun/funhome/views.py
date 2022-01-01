import os
from datetime import datetime

import magic
import pytz
from django.conf import settings
from django.contrib.auth.models import User
from django.core import serializers
from django.core.files import File
from django.http import (FileResponse, Http404, HttpResponse,
                         HttpResponseBadRequest, HttpResponseForbidden,
                         JsonResponse)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import translation
from django.utils.translation import gettext_lazy as _
# Create your views here.
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)
from funfile.models import Checkup

from .apps import FunhomeConfig
from .modelforms import FunhomestickerModelForm, HomestickerModelForm
from .models import (Appreciation, Funhomesticker, Homesticker,
                     appreciation_name, funhomesticker_name, homesticker_name)

home_template = 'funhome/home.html'
homesticker_create_template = f'funhome/homesticker_create.html'
homesticker_detail_template = f'funhome/homesticker_detail.html'
homesticker_delete_template = f'funhome/homesticker_delete.html'
homesticker_update_template = f'funhome/homesticker_update.html'
homesticker_list_template = f'funhome/homesticker_list.html'
funhomesticker_create_template = f'funhome/funhomesticker_create.html'
funhomesticker_detail_template = f'funhome/funhomesticker_detail.html'
funhomesticker_delete_template = f'funhome/funhomesticker_delete.html'
funhomesticker_update_template = f'funhome/funhomesticker_update.html'
funhomesticker_list_template = f'funhome/funhomesticker_list.html'
appreciation_detail_template = f'funhome/appreciation_detail.html'
data_privacy_template = 'funhome/data_privacy.html'
legal_information_template = 'funhome/legal_information.html'
data_privacy_example_template = 'funhome/data_privacy.html.example'
legal_information_example_template = 'funhome/legal_information.html.example'
data_privacy_template_path = os.path.join(
    settings.BASE_DIR, 'templates', 'funhome', 'data_privacy.html')
legal_information_template_path = os.path.join(
    settings.BASE_DIR, 'templates', 'funhome', 'legal_information.html')


class HomestickerListView(ListView):
    model = Homesticker
    form_class = HomestickerModelForm
    template_name = homesticker_list_template

    ordering = ['-promulgating_date', ]

    paginate_by = 8
    paginate_orphans = 1
    context_object_name = 'homestickers'

    def get_queryset(self):
        queryset = Homesticker.objects.filter(
            is_hidden=False).order_by('-promulgating_date')
        return queryset


class HomestickerDetailView(DetailView):
    model = Homesticker
    form_class = HomestickerModelForm
    template_name = homesticker_detail_template

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        file_path = os.path.join(settings.MEDIA_ROOT, str(
            context_data['object'].content_file.name))
        context_data['is_video'] = str(magic.from_file(
            file_path, mime=True)).startswith('video/')
        return context_data


class FunhomestickerListView(ListView):
    model = Funhomesticker
    form_class = FunhomestickerModelForm
    template_name = funhomesticker_list_template

    ordering = ['-promulgating_date', ]

    paginate_by = 8
    paginate_orphans = 1
    context_object_name = 'funhomestickers'

    def get_queryset(self):
        queryset = Funhomesticker.objects.filter(
            is_hidden=False).order_by('-promulgating_date')
        return queryset


class FunhomestickerDetailView(DetailView):
    model = Funhomesticker
    form_class = FunhomestickerModelForm
    template_name = funhomesticker_detail_template


class HomeView(TemplateView):
    template_name = home_template

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        funhomestickers = Funhomesticker.objects.filter(
            is_hidden=False).order_by('-promulgating_date')[:8]
        if funhomestickers.count() < 1:
            funhomestickers = [get_default_funhomesticker()]
            context_data['is_funhomestickers_null'] = True
        context_data['funhomestickers'] = funhomestickers
        context_data['appreciations'] = Appreciation.objects.order_by(
            'submitting_date')[:4]
        return context_data


class AppreciationDetailView(DetailView):
    model = Appreciation
    template_name = appreciation_detail_template


def get_all_bootswatch_themes(request):
    if request.method == 'GET':
        return JsonResponse(
            os.listdir(os.path.join(settings.BASE_DIR, 'static', 'libs',
                                    'bootswatch', 'dist')), safe=False)


def get_favicon_ico(request):

    file_path = os.path.join(
        settings.SERVE_STATIC_ROOT,
        'images',
        'x_dove.webp')

    if os.path.exists(file_path):
        content_type = magic.from_file(file_path, mime=True)
        return FileResponse(open(file_path, 'rb'), content_type=content_type)
    else:
        return HttpResponse()


def get_default_homesticker():
    default_carousel_image_path = os.path.join(
        settings.SERVE_STATIC_ROOT, 'images', 'default_carousel_image.webp')
    default_carousel_content_file_path = os.path.join(
        settings.SERVE_STATIC_ROOT, 'media', 'default_carousel_content_file.pdf')
    return Homesticker(
        title=_('X-DOVE'),
        subtitle=_('Larry`s sharing'),
        cover=os.path.exists(default_carousel_image_path) and
        File(open(default_carousel_image_path)) or None,
        promulgator=User.objects.get(is_superuser=True),
        content_file=os.path.exists(default_carousel_content_file_path) and
        File(open(default_carousel_content_file_path)) or None,
        promulgating_date=datetime(2005, 7, 14, 12, 30),
        comment=_('larry'))


def data_privacy(request):
    if request.method == 'GET':
        return render(
            request,
            os.path.exists(data_privacy_template_path) and
            data_privacy_template or
            data_privacy_example_template)


def legal_information(request):
    if request.method == 'GET':
        return render(
            request,
            os.path.exists(legal_information_template_path) and
            legal_information_template or
            legal_information_example_template)


def get_default_funhomesticker():
    default_carousel_image_path = os.path.join(
        settings.SERVE_STATIC_ROOT, 'images', 'default_carousel_image.webp')
    return Funhomesticker(
        title=_('X-DOVE'),
        subtitle=_('Larry`s sharing'),
        cover=os.path.exists(default_carousel_image_path) and
        File(open(default_carousel_image_path)) or None,
        promulgator=None,
        content='',
        promulgating_date=datetime(2005, 7, 14, 12, 30),
        comment=_('larry'))
