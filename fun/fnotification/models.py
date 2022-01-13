import hashlib
import os
import uuid

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import (RichTextUploadingField,
                                      RichTextUploadingFormField)
from django import forms
from django.contrib.auth.models import Group, User
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import *
from django.db import models
from django.utils.translation import gettext_lazy as _
from funfile.storage import upload_to
from funuser.models import Funuser

# Create your models here.


class Fnotification(models.Model):

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')

    def __str__(self):
        return self.title

    def clean(self):
        self.content = bleach_clean(self.content)

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    title = models.CharField(
        max_length=64, blank=False, verbose_name=_('Title'))

    receiving_groups = models.ManyToManyField(
        Group, verbose_name=_('groups'), blank=True,
        related_name="notification_set",
        related_query_name="notification",
        help_text=_(
            'The groups this notification belongs to. all user of specific '
            'groups will receive notification. for all users if groups is null'
        ),
    )

    readers = models.ManyToManyField(
        to=Funuser, verbose_name=_('Reader'), blank=True,
        related_name="reader_set",
        related_query_name="reader",)

    content = RichTextUploadingField(
        max_length=2048,
        verbose_name=_('Content'))

    additional_files = models.FileField(
        verbose_name=_('Additional files'),
        help_text=_('If you have more than one file, please package them and '
                    'upload them.'),)

    DOC = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date of creating'))

    DOU = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Date of updating'))

    comment = models.TextField(
        max_length=128,
        verbose_name=_('Comment'))

    poster = models.ForeignKey(
        to=Funuser, on_delete=models.CASCADE, verbose_name=_('Author'))
