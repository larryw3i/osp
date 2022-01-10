import math
import os
import uuid
from datetime import datetime

import bleach
import magic
import pytz
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import paginator
from django.core.exceptions import ValidationError
from django.core.paginator import InvalidPage, Paginator
from django.db.models import F, Q
from django.http import Http404
from django.shortcuts import (Http404, HttpResponseRedirect, redirect, render,
                              reverse)
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from .modelforms import FblogModelForm
from .models import Fblog

# Create your views here.


class FblogListView(LoginRequiredMixin, ListView):
    model = Fblog
    form_class = FblogModelForm
    template_name = 'funblog/funblog_list.html'
    ordering = ['-DOC', ]
    paginate_by = 5
    paginate_orphans = 1

    def paginate_queryset(self, queryset, page_size):

        paginator = self.get_paginator(
            queryset, page_size,
            orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())

        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or \
            self.request.GET.get(page_kwarg) or 1

        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(
                    _("Page is not 'last', nor can it be converted to an int."))
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            page = paginator.page(1)
            return (paginator, page, page.object_list, page.has_other_pages())


class FblogCreateView(LoginRequiredMixin, CreateView):
    model = Fblog
    form_class = FblogModelForm
    template_name = 'funblog/funblog_create.html'
    success_url = reverse_lazy('funblog:fblog_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
