import os
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from funfile.storage import upload_to
from imagekit.models import ImageSpecField

# Create your models here.


funuser_mame = 'funuser'


class Funuser(AbstractUser):

    avatar = models.ImageField(
        upload_to=upload_to, blank=True, verbose_name=_('Avatar'), )

    birth_date = models.DateField(
        blank=True, null=True, verbose_name=_('Brith date'))
    is_birth_date_outward = models.BooleanField(
        default=False, verbose_name=_('Is outward') + ' ?')

    address = models.CharField(
        blank=True, max_length=64, verbose_name=_('Address'))
    is_address_outward = models.BooleanField(
        default=False, verbose_name=_('Is outward') + ' ?')

    hometown = models.CharField(
        blank=True, max_length=64, verbose_name=_('Hometown'))
    is_hometown_outward = models.BooleanField(
        default=False, verbose_name=_('Is outward') + ' ?')

    college = models.CharField(
        blank=True, max_length=64, verbose_name=_('College'))

    is_college_outward = models.BooleanField(
        default=False, verbose_name=_('Is outward') + ' ?')

    occupation = models.CharField(
        blank=True, max_length=64, verbose_name=_('Occupation'))
    is_occupation_outward = models.BooleanField(
        default=False, verbose_name=_('Is outward') + ' ?')

    hobby = models.CharField(blank=True, max_length=64,
                             verbose_name=_('Hobby'))
    is_hobby_outward = models.BooleanField(
        default=False, verbose_name=_('Is outward') + ' ?')

    motto = models.CharField(blank=True, max_length=64,
                             verbose_name=_('Motto'))

    is_motto_outward = models.BooleanField(
        default=False, verbose_name=_('Is outward') + ' ?')
