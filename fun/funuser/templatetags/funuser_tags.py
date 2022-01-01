
from django import template
from django.conf import settings
from funuser.models import Funuser

register = template.Library()


@register.simple_tag(takes_context=True)
def get_funuser_name(context, user):
    funuser = Funuser.objects.filter(user=user).first()
    return funuser.full_name if (funuser and len(funuser.full_name) > 0) \
        else user.username


@register.simple_tag(takes_context=True)
def get_funuser_avatar_url(context, user):
    request = context['request']
    return reverse(
        'funfile:get_file', kwargs={"file_id": request.user.avatar.name}
    ) if (len(request.user.avatar.name) > 0) else \
        (settings.STATIC_URL + 'images/x_dove.webp')
