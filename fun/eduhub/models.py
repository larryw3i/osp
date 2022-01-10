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

# Create your models here.

label_name = 'label'
funtest_name = 'funtest'
content_name = 'content'
funcontent_name = 'funcontent'
eduhubhomesticker_name = 'eduhubhomesticker'
classification_name = 'classification'


#  _____                            _             _
# |  ___|   _ _ __   ___ ___  _ __ | |_ ___ _ __ | |_
# | |_ | | | | '_ \ / __/ _ \| '_ \| __/ _ \ '_ \| __|
# |  _|| |_| | | | | (_| (_) | | | | ||  __/ | | | |_
# |_|   \__,_|_| |_|\___\___/|_| |_|\__\___|_| |_|\__|

class Classification(models.Model):
    class Meta:
        verbose_name = _('Classification')
        verbose_name_plural = _('Classifications')

    def __str__(self):
        return (
            '' if self.parent is None
            else str(self.parent) + '/'
        ) + _(self.name)

    def clean(self):
        if '/' in self.name:
            raise ValidationError({
                'name': _("name includes '/' is not allowed")})

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    parent = models.ForeignKey(
        to='self', null=True, blank=True, on_delete=models.CASCADE,
        verbose_name=_('Parent classification'))

    name = models.CharField(
        max_length=64, blank=False,
        verbose_name=_("Classification name('/' cannot be included)"))

    comment = models.CharField(
        null=True, blank=True,
        max_length=64, verbose_name=_('Classification comment'))


def label_upload_to(instance, filename):
    return '{0}/{1}'.format(instance.author.username, filename)

class Label(models.Model):

    class Meta:
        verbose_name = _('Eduhub label')
        verbose_name_plural = _('Eduhub  labels')

    def __str__(self):
        return self.name

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(
        max_length=64, blank=False,
        verbose_name=_('Label name'))
    comment = models.CharField(
        max_length=64, verbose_name=_('Label comment'))
    cover = models.ImageField(
        upload_to=label_upload_to, blank=True, verbose_name=_('Label cover'))
    creating_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Label creating date'))
    author = models.ForeignKey(
        to=Funuser, on_delete=models.CASCADE, verbose_name=_('Label author'))
    is_legal = models.BooleanField(
        default=True, verbose_name=_('Is label legal') + " ?")


class Funcontent(models.Model):

    class Meta:
        verbose_name = _('Eduhub content (NEW)')
        verbose_name_plural = _('Eduhub contents (NEW)')

    def __str__(self):
        return self.title

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)

    label = models.ForeignKey(
        to=Label, on_delete=models.SET_NULL, null=True,
        verbose_name=_('Content label'))

    classification = models.ForeignKey(
        to=Classification, blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name=_('Content classification'))

    title = models.CharField(max_length=64, blank=False,
                             verbose_name=_('Content title'))

    content = RichTextUploadingField(max_length=2048,
                                     verbose_name=_('Content'))

    uploading_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Content uploading date'))
    comment = models.TextField(
        max_length=64, verbose_name=_('Content comment'))
    is_legal = models.BooleanField(
        default=True, verbose_name=_('Is content legal'))


def eduhubhomesticker_upload_to(instance, filename):
    return '{0}/{1}'.format(instance.promulgator.username, filename)

class Eduhubhomesticker(models.Model):
    class Meta:
        verbose_name = _('Eduhub homepage sticker')
        verbose_name_plural = _('Eduhub homepage stickers')

    def __str__(self):
        return self.title

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False,)
    title = models.CharField(
        max_length=32,
        verbose_name=_('Eduhub homepage sticker title'))

    subtitle = models.TextField(
        max_length=64,
        verbose_name=_('Eduhub homepage sticker subtitle'))

    cover = models.ImageField(
        upload_to=eduhubhomesticker_upload_to,
        verbose_name=_('Eduhub homepage sicker cover'))

    promulgator = models.ForeignKey(
        to=Funuser, on_delete=models.CASCADE,
        verbose_name=_('Eduhub homepage sticker promulgator'))

    description = RichTextUploadingField()

    content = RichTextUploadingField()

    promulgating_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Eduhub homepage sticker promulgating date'))

    comment = models.TextField(max_length=128, verbose_name=_(
        'Eduhub homepage sticker comment'))

    is_hidden = models.BooleanField(
        default=False, verbose_name=_('Hidden') + " ?")


class Funtest(models.Model):

    class Meta:
        verbose_name = _('Eduhub Test')
        verbose_name_plural = _('Eduhub Tests')

    def __str__(self):
        return self.name

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        editable=False, unique=True)

    test_title = models.CharField(
        max_length=64, blank=True, null=True,
        verbose_name=_('Test commit'))

    test_owner = models.ForeignKey(
        to=Funuser, on_delete=models.CASCADE,
        verbose_name=_('Test owner'))

    test_text = models.TextField(
        max_length=12288,
        verbose_name=_('Template text'))

    submitting_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Test submitting date'))

    last_modifying_date = models.DateTimeField(
        blank=True, null=True,
        verbose_name=_('Last modifying date'))

    test_commit = models.CharField(
        max_length=64, blank=True, null=True,
        verbose_name=_('Test commit'))


#
#     _                          _     _
#    / \   _ __  _ __  _ __ __ _(_)___(_)_ __   __ _
#   / _ \ | '_ \| '_ \| '__/ _` | / __| | '_ \ / _` |
#  / ___ \| |_) | |_) | | | (_| | \__ \ | | | | (_| |
# /_/   \_\ .__/| .__/|_|  \__,_|_|___/_|_| |_|\__, |
#         |_|   |_|                            |___/

class Appraising(models.Model):
    class Meta:
        verbose_name = _('Appraising')
        verbose_name_plural = _('Appraisings')

    def __str__(self):
        return str(self.amember) + _(' appraise ') + str(self.acontent)

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    amember = models.ForeignKey(
        to='ASharingGroupMember',
        on_delete=models.CASCADE,
        verbose_name=_('Appraisings from'))
    acontent = models.ForeignKey(
        to='ASharingContent', on_delete=models.CASCADE,
        verbose_name=_('Content'))
    appraising_point = {'min': 0, 'max': 10}
    point = models.SmallIntegerField(
        default=appraising_point['min'],
        validators=[
            MinValueValidator(appraising_point['min']),
            MaxValueValidator(appraising_point['max'])])
    DOA = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date of Appraising'))
    comment = models.CharField(
        max_length=64, verbose_name=_('Comment'))


class ASharingContent(models.Model):
    class Meta:
        verbose_name = _('Appraising content')
        verbose_name_plural = _('Appraising contents')

    def __str__(self):
        return self.title

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    cfrom = models.ForeignKey(
        to=Funuser, on_delete=models.CASCADE, verbose_name=_('Content from'))

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
    agroup = models.ForeignKey(
        to='ASharingGroup', on_delete=models.CASCADE, null=False, blank=False,
        verbose_name=_('Classification'))
    classification = models.ForeignKey(
        to=Classification, on_delete=models.SET_NULL, null=True,
        verbose_name=_('Classification'))

    comment = models.TextField(max_length=128, verbose_name=_(
        'Eduhub homepage sticker comment'))

    is_legal = models.BooleanField(
        default=True, verbose_name=_('Is content legal'))

def asharinggroup_upload_to(instance, filename):
    return '{0}/{1}'.format(instance.founder.username, filename)

class ASharingGroup(models.Model):
    class Meta:
        verbose_name = _('ASharingGroup')
        verbose_name_plural = _('ASharingGroups')

    def __str__(self):
        return self.name
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(
        max_length=64, blank=False, verbose_name=_('Name'))
    subtitle = models.CharField(
        max_length=64, blank=False, verbose_name=_('Subtitle'))
    cover = models.ImageField(
        upload_to=asharinggroup_upload_to, blank=True, verbose_name=_('Group cover'))
    founder = models.ForeignKey(
        to=Funuser, on_delete=models.CASCADE,
        verbose_name=_('ASharingGroup Founder'))
    comment = models.CharField(
        max_length=64, verbose_name=_('ASharingGroup Comment'))
    DOC = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date of creating'))
    is_legal = models.BooleanField(
        default=True, verbose_name=_('Is legal?'))


class ASGMemberClassification(models.Model):
    class Meta:
        verbose_name = _('ASharingGroup member Classification')
        verbose_name_plural = _('ASharingGroup member Classifications')

    def __str__(self):
        return ('' if self.parent is None
                else str(self.parent) + '/'
                ) + _(self.cname)

    def clean(self):
        if '/' in self.cname:
            raise ValidationError({
                'name': _("name includes '/' is not allowed")})
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    parent = models.ForeignKey(
        to='self', null=True, blank=True, on_delete=models.SET_NULL,
        verbose_name=_('Parent classification'))
    cname = models.CharField(
        max_length=64,
        blank=False,
        verbose_name=_('Classification Name'))
    comment = models.CharField(
        null=True, blank=True,
        max_length=64, verbose_name=_('Classification Comment'))


class ASharingGroupMember(models.Model):
    class Meta:
        verbose_name = _('ASharingGroup member')
        verbose_name_plural = _('ASharingGroup members')

    def __str__(self):
        return self.mname

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    mname = models.CharField(
        max_length=64, blank=False,
        verbose_name=_('Member Name'))
    funuser = models.ForeignKey(
        null=False,
        to=Funuser, on_delete=models.CASCADE, verbose_name=_('funuser'))
    agroup = models.ForeignKey(
        to='ASharingGroup', on_delete=models.CASCADE,
        verbose_name=_('ASharing group'))
    gclassification = models.ManyToManyField(
        to='ASGMemberClassification', blank=True,
        verbose_name=_('classifications'))
    isjudge = models.BooleanField(
        default=False, verbose_name=_('Is judge ?'))
    applyinginfo = models.CharField(
        max_length=64, blank=False, verbose_name=_('applying info'))
    enable = models.BooleanField(
        default=False, verbose_name=_('Is member enable?'))
    DOJ = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Date of joining'))
