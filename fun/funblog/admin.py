
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.shortcuts import (Http404, HttpResponseRedirect, redirect, render,
                              reverse)
from django.utils.translation import gettext_lazy as _

from fun import bleach_clean

from .models import Fblog

# Register your models here.


@admin.register(Fblog)
class FblogAdmin(admin.ModelAdmin):
    fields = ('title', 'content', 'comment', 'is_legal')
    ordering = ('-DOC', '-DOU')
    list_display = ('title', 'DOC', 'DOU', 'is_legal')
    search_fields = ['title', 'content']
