from django import forms
from django.contrib import admin

from fun import bleach_clean

from .modelforms import FunhomestickerModelForm, HomestickerModelForm
from .models import Appreciation, Funhomesticker, Homesticker

# Register your models here.


@admin.register(Homesticker)
class HomestickerAdmin(admin.ModelAdmin):
    fields = ['title', 'subtitle', 'cover', 'content_file',
              'comment', 'is_hidden']
    list_display = ('title', 'promulgator',
                    'promulgating_date', 'is_hidden')
    list_per_page = 10
    ordering = ('-promulgating_date',)

    def save_model(self, request, obj, form, change):
        obj.promulgator = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Funhomesticker)
class HomestickerAdmin(admin.ModelAdmin):
    fields = ['title', 'subtitle', 'cover', 'content', 'comment', 'is_hidden']
    list_display = ('title', 'promulgator',
                    'promulgating_date', 'is_hidden')
    list_per_page = 10
    ordering = ('-promulgating_date',)
    formfield_overrides = {
        Funhomesticker.title: {'widget': forms.TextInput(
            attrs={'autocomplete': 'off'})},
    }

    def save_model(self, request, obj, form, change):
        obj.content = bleach_clean(obj.content)
        obj.promulgator = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Appreciation)
class AppreciationAdmin(admin.ModelAdmin):
    fields = [
        'invitee',
        'invitee_title',
        'brief_comment',
        'illustration',
        'home_comment',
        'content',
    ]

    list_display = (
        'brief_comment', 'invitee', 'home_comment',)

    list_per_page = 5

    ordering = ('-submitting_date', )

    def save_model(self, request, obj, form, change):
        obj.content = bleach_clean(obj.content)
        obj.submitter = request.user
        return super().save_model(request, obj, form, change)
