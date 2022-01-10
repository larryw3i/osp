
import math

from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.fields import (RichTextUploadingField,
                                      RichTextUploadingFormField)
from django import forms
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.core.exceptions import ValidationError
from django.forms import ImageField, ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Fblog


class FblogModelForm(ModelForm):
    class Meta:
        model = Fblog
        fields = ['title', 'content', 'comment']
        labels = {
            'title': _('title'),
            'comment': _('Comment')
        }
