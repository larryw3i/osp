import hashlib
import os
import random
import time
import uuid
from functools import partial
from urllib.parse import urljoin

from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
from django.core.files import File, locks
from django.core.files.move import file_move_safe
from django.core.files.storage import FileSystemStorage
from django.core.signals import setting_changed
from django.db import models
from django.http import HttpResponse
from django.utils import timezone
from django.utils._os import safe_join
from django.utils.crypto import get_random_string
from django.utils.deconstruct import deconstructible
from django.utils.encoding import filepath_to_uri
from django.utils.functional import LazyObject, cached_property
from django.utils.module_loading import import_string
from django.utils.text import get_valid_filename
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Checkup(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True,
                          default=uuid.uuid4, editable=False)
    file_id = models.UUIDField(help_text='file uuid')
    is_legal = models.BooleanField(default=True, help_text='is legal')
    comment = models.TextField(help_text='comment')
