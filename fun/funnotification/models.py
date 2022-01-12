from django.db import models
from django.contrib.auth.models import Group

# Create your models here.


class Fnotification():

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')

    def __str__(self):
        return self.title

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    
    title = models.CharField(
        max_length=64, blank=False,verbose_name=_('Title'))
    
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )

    content = RichTextUploadingField(
        max_length=2048,
        verbose_name=_('Content'))

    additional_files= FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        verbose_name=_('Additional files'))

    DOC = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date of creating'))

    DOU = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Date of updating'))

    comment = models.TextField(
        max_length=128,
        verbose_name=_('Comment'))

    poster = models.ForeignKey(
        to=Funuser, on_delete=models.CASCADE, verbose_name=_('Author'))