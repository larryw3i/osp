import uuid

from ckeditor.fields import RichTextField
from ckeditor_uploader import fields
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from funfile.storage import upload_to
from funuser.models import Funuser

# Put the readability of your code first
# Create your models here.

homesticker_name = 'homesticker'
funhomesticker_name = 'funhomesticker'
appreciation_name = 'appreciation'


class Homesticker(models.Model):

    class Meta:
        verbose_name = _(
            'Home sticker(deprecation)')
        verbose_name_plural = _(
            'Home sticker(deprecation)')

    def __str__(self):
        return self.title

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        editable=False,)

    title = models.CharField(
        max_length=32, verbose_name=_('Sticker title'))

    subtitle = models.TextField(
        max_length=64, verbose_name=_('Sticker subtitle'))

    cover = models.ImageField(
        upload_to=upload_to, verbose_name=_('Sticker cover'))

    promulgator = models.ForeignKey(
        to=Funuser, on_delete=models.CASCADE,
        verbose_name=_('Sticker promulgator'))

    content_file = models.FileField(
        upload_to=upload_to, verbose_name=_('Sticker content file'))

    promulgating_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Sticker promulgating date'))

    comment = models.TextField(
        max_length=128,
        verbose_name=_('Sticker comment'))

    is_hidden = models.BooleanField(
        default=False,
        verbose_name=_('Hidden') + " ?")


class Funhomesticker(models.Model):

    class Meta:
        verbose_name = _('Home sticker') + f'({_("NEW")})'
        verbose_name_plural = _('Home stickers') + f'({_("NEW")})'

    def __str__(self):
        return self.title

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,)

    title = models.CharField(
        max_length=32,
        verbose_name=_('Sticker title'))

    subtitle = models.TextField(
        max_length=64,
        verbose_name=_('Sticker subtitle'))

    cover = models.ImageField(
        upload_to=upload_to,
        verbose_name=_('Sticker cover'))

    promulgator = models.ForeignKey(
        to=Funuser,
        on_delete=models.CASCADE,
        verbose_name=_('Sticker promulgator'))

    content = fields.RichTextUploadingField()

    promulgating_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Sticker promulgating date'))

    comment = models.TextField(
        max_length=128, verbose_name=_('Sticker comment'))

    is_hidden = models.BooleanField(
        default=False, verbose_name=_('Hidden') + " ?")


class Appreciation(models.Model):

    class Meta:
        verbose_name = _('Appreciation')
        verbose_name_plural = _('Appreciation')

    def __str__(self):
        return self.brief_comment

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    invitee = models.CharField(
        max_length=8,
        verbose_name=_('invitee')
    )

    invitee_title = models.CharField(
        max_length=8,
        verbose_name=_('invitee title')
    )

    brief_comment = models.CharField(
        max_length=16,
        verbose_name=_('brief comment')
    )

    illustration = models.ImageField(
        upload_to=upload_to,
        verbose_name=_('illustration')
    )

    home_comment = models.TextField(
        max_length=128,
        verbose_name=_('home comment'),
    )

    content = fields.RichTextUploadingField(
        max_length=4096,
        verbose_name=_('appreciation content')
    )

    submitter = models.ForeignKey(
        to=Funuser,
        on_delete=models.CASCADE,
        verbose_name=_('Submitter')
    )

    submitting_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Submitting date')
    )
