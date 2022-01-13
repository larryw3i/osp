import os
import re
import urllib
import uuid

from django import template
from django.conf import settings
from django.utils.translation import gettext_lazy as _

register = template.Library()

