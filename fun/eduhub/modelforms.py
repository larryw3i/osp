
import math

from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.fields import (RichTextUploadingField,
                                      RichTextUploadingFormField)
from django import forms
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.core.exceptions import ValidationError
from django.forms import ImageField, ModelForm
from django.utils.translation import gettext_lazy as _

from .models import (Appraising, ASGMemberClassification, ASharingContent,
                     ASharingGroup, ASharingGroupMember, Classification,
                     Eduhubhomesticker, Funcontent, Funtest, Label)

#     _                          _     _
#    / \   _ __  _ __  _ __ __ _(_)___(_)_ __   __ _
#   / _ \ | '_ \| '_ \| '__/ _` | / __| | '_ \ / _` |
#  / ___ \| |_) | |_) | | | (_| | \__ \ | | | | (_| |
# /_/   \_\ .__/| .__/|_|  \__,_|_|___/_|_| |_|\__, |
#         |_|   |_|                            |___/
#  __  __           _      _ _____
# |  \/  | ___   __| | ___| |  ___|__  _ __ _ __ ___
# | |\/| |/ _ \ / _` |/ _ \ | |_ / _ \| '__| '_ ` _ \
# | |  | | (_) | (_| |  __/ |  _| (_) | |  | | | | | |
# |_|  |_|\___/ \__,_|\___|_|_|  \___/|_|  |_| |_| |_|


class AppraisingModelForm(ModelForm):
    class Meta:
        model = Appraising
        fields = ['point', 'comment']

        widgets = {
            'comment': forms.Textarea(attrs={'rows': '2'}),
            'point': forms.NumberInput(attrs={
                'min': Appraising.appraising_point['min'],
                'max': Appraising.appraising_point['max']})
        }

    def clean(self):
        pass


class ASharingCModelForm(ModelForm):
    class Meta:
        model = ASharingContent
        fields = ['title', 'content', 'classification']
        labels = {
            'classification': _('Sharing Content classification'),
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'autocomplete': 'off',
                'placeholder': _('Content title'),
                'class': 'text-center'}),
            'comment': forms.Textarea(attrs={'rows': '3'})
        }

    def clean(self):
        pass


class ASharingGroupModelForm(ModelForm):
    class Meta:
        model = ASharingGroup
        fields = ['name', 'subtitle', 'comment']

        labels = {
            'name': _('ASharingGroup name'),
            'subtitle': _('ASharingGroup subtitle'),
            'comment': _('ASharingGroup comment'),
        }


class ASGMemberClassificationModelForm(ModelForm):
    class Meta:
        model = ASGMemberClassification
        fields = ['parent', 'cname', 'comment']

        labels = {
            'parent': _('Parent classification'),
            'cname': _('Classification Name'),
            'comment': _('Classification Comment'),
        }


class ASGMemberModelForm(ModelForm):
    class Meta:
        model = ASharingGroupMember
        fields = ['applyinginfo']

        labels = {
            'applyinginfo': _('applying info'),
        }


class LabelModelForm(ModelForm):
    class Meta:
        model = Label
        fields = ['name', 'cover', 'comment']

        labels = {
            'name': _('Label name'),
            'cover': _('Cover image'),
            'comment': _('Comment'),
        }

        widgets = {
            'cover': forms.FileInput(attrs={'class': 'preview-image'})
        }


class FuncontentModelForm(ModelForm):
    class Meta:
        model = Funcontent
        fields = ['title', 'content', 'comment', 'classification']
        labels = {
            'title': '',
            'content': _('Content'),
            'comment': _('Comment'),
            'classification': _('Content classification'),
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'autocomplete': 'off',
                'placeholder': _('Content title'),
                'class': 'text-center'}),
            'comment': forms.Textarea(attrs={'rows': '5'})
        }


class EduhubhomestickerModelForm(ModelForm):

    class Meta:

        model = Eduhubhomesticker
        fields = ['title', 'cover', 'content', 'comment', 'description']

        labels = {
            'title': _('Sticker title'),
            'cover': _('Sticker Cover'),
            'content': _('Sticker content'),
            'comment': _('Sticker Comment'),
            'description': _('description'),
        }

        widgets = {
            'comment': forms.Textarea(attrs={'rows': '5'}),
        }


class FuntestModelForm(ModelForm):
    class Meta:
        model = Funtest
        fields = ['test_title', 'test_text', 'test_commit']

        widgets = {
            'test_text': forms.Textarea(attrs={'rows': '25'}),
        }


class ClassificationModelForm(ModelForm):
    class Meta:
        model = Classification
        fields = ['parent', 'name', 'comment']

    def clean(self):
        if Classification.objects\
                .filter(
                    name=self.cleaned_data['name'],
                    parent=self.cleaned_data['parent'])\
                .exists():
            raise ValidationError({'name': _("name exists")})
