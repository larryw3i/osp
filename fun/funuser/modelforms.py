

import math

from django import forms
from django.forms import ImageField, ModelForm
from django.utils.formats import ISO_INPUT_FORMATS
from django.utils.translation import gettext_lazy as _

from .models import Funuser


class FunuserModelForm(ModelForm):
    class Meta:
        model = Funuser
        exclude = ['user', ]

        fields = ['avatar', 'birth_date', 'first_name', 'last_name', 'address',
                  'hometown', 'college',
                  'occupation',
                  'hobby',
                  'motto',
                  'is_birth_date_outward',
                  'is_address_outward',
                  'is_hometown_outward',
                  'is_college_outward',
                  'is_occupation_outward',
                  'is_hobby_outward',
                  'is_motto_outward']

        widgets = {
            'avatar': forms.FileInput(
                attrs={'class': 'custom-file-input',
                       'aria-describedby': "avatarInputGroupFileAddon",
                       'accept': 'image/*',
                       'src-for': '#id_avatar_show'}),
            'birth_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control text-right'}),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'hometown': forms.TextInput(attrs={'class': 'form-control'}),
            'college': forms.TextInput(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'hobby': forms.TextInput(attrs={'class': 'form-control'}),
            'motto': forms.TextInput(attrs={'class': 'form-control'}),
            'is_birth_date_outward': forms.CheckboxInput(
                attrs={'class': 'custom-control-input', 'type': 'checkbox', }),
            'is_address_outward': forms.CheckboxInput(
                attrs={'class': 'custom-control-input', 'type': 'checkbox', }),
            'is_hometown_outward': forms.CheckboxInput(
                attrs={'class': 'custom-control-input', 'type': 'checkbox', }),
            'is_college_outward': forms.CheckboxInput(
                attrs={'class': 'custom-control-input', 'type': 'checkbox', }),
            'is_occupation_outward': forms.CheckboxInput(
                attrs={'class': 'custom-control-input', 'type': 'checkbox', }),
            'is_hobby_outward': forms.CheckboxInput(
                attrs={'class': 'custom-control-input', 'type': 'checkbox', }),
            'is_motto_outward': forms.CheckboxInput(
                attrs={'class': 'custom-control-input', 'type': 'checkbox', }),
        }
