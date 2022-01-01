
# Create your views here.

import math
import os

import magic
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core import paginator
from django.core.exceptions import ValidationError
from django.core.files import File
from django.http import Http404
from django.shortcuts import (Http404, HttpResponseRedirect, redirect, render,
                              reverse)
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .apps import FunuserConfig
from .modelforms import FunuserModelForm
from .models import Funuser, funuser_mame

funuser_create_template = f'funuser/funuser_create.html'
funuser_detail_template = f'funuser/funuser_detail.html'
funuser_delete_template = f'funuser/funuser_delete.html'
funuser_update_template = f'funuser/funuser_update.html'
funuser_list_template = f'funuser/funuser_list.html'


class FunuserUpdateView(LoginRequiredMixin, UpdateView):
    model = Funuser
    form_class = FunuserModelForm
    template_name = funuser_update_template
    success_url = reverse_lazy('funuser:funuser_update')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):

        if not Funuser.objects.filter(
                user=self.request.user, id=form.instance.id).exists():
            form.add_error('full_name', _('Nice try'))
            return render(
                self.request, funuser_update_template, context={'form': form})
        return super().form_valid(form)


class FunuserDetailView(LoginRequiredMixin, DetailView):
    model = Funuser
    template_name = funuser_detail_template
    pk_url_kwarg = 'user_id'
