# Create your models here.
import hashlib
import os
import uuid

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import (RichTextUploadingField,
                                      RichTextUploadingFormField)
from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import *
from django.db import models
from django.utils.translation import gettext_lazy as _
from funfile.storage import upload_to
from funuser.models import Funuser

from fun import bleach_clean

# Create your models here.


class Fblog(models.Model):
    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')

    def __str__(self):
        return self.title

    def clean(self):
        self.content = bleach_clean(self.content)

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    title = models.CharField(max_length=64, blank=False,
                             verbose_name=_('Title'))

    content = RichTextUploadingField(
        max_length=2048,
        verbose_name=_('Content'))

    DOC = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date of appraising content creating'))

    DOU = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Date of appraising content updating'))

    comment = models.TextField(max_length=128, verbose_name=_(
        'Eduhub homepage sticker comment'))
    
    author = models.ForeignKey(
        to=Funuser, on_delete=models.CASCADE, verbose_name=_('Author'))

    is_legal = models.BooleanField(
        default=True, verbose_name=_('Is content legal?'))
