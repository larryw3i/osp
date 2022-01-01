
import math

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import (RichTextUploadingField,
                                      RichTextUploadingFormField)
from django import forms
from django.forms import ImageField, ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Appreciation, Funhomesticker, Homesticker


class HomestickerModelForm(ModelForm):

    class Meta:

        model = Homesticker
        fields = ['title', 'cover', 'content_file', 'comment']

        labels = {
            'title': _('Sticker title'),
            'cover': _('Sticker Cover'),
            'content_file': _('Sticker content file'),
            'comment': _('Sticker Comment'),
        }

        help_texts = {
            'content_file':
            _('content file, pdf and video file is allowed only')
        }

        widgets = {
            'content_file': forms.FileInput(
                attrs={
                    'class': 'preview-pdf preview-video',
                    'accept': 'video/*, .pdf'}),
            'comment': forms.Textarea(
                attrs={
                    'rows': '5'}),
        }


class FunhomestickerModelForm(ModelForm):

    class Meta:

        model = Funhomesticker
        fields = ['title', 'cover', 'content', 'comment']

        labels = {
            'title': _('Sticker title'),
            'cover': _('Sticker Cover'),
            'content': _('Sticker content'),
            'comment': _('Sticker Comment'),
        }

        widgets = {
            'comment': forms.Textarea(attrs={'rows': '5'}),
        }


class AppreciationModelForm(ModelForm):
    class Meta:
        model = Appreciation
        fields = [
            'invitee',
            'invitee_title',
            'brief_comment',
            'illustration',
            'home_comment',
            'content',
        ]

        widgets = {
            'home_comment': forms.Textarea(attrs={'rows': '3'}),
        }
