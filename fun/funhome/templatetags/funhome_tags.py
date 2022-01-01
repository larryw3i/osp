
from django import template
from django.utils.translation import gettext_lazy as _

from fun import settings

register = template.Library()

bootstrap_css_url = 'bootstrap/dist/css/bootstrap.min.css'


@register.simple_tag(takes_context=True)
def bootswatch_css_url(theme):
    return f'bootswatch/dist/{theme}/bootstrap.min.css'


@register.simple_tag(takes_context=True)
def get_current_theme_url(context):
    theme = context['request'].COOKIES.get('theme', 'default')
    return ('/static/node_modules/' + (bootstrap_css_url if theme == 'default'
                                       else bootswatch_css_url(theme)))


@register.simple_tag(takes_context=True)
def get_current_theme_name(context):
    return _(context['request'].COOKIES.get('theme', 'default'))


@register.simple_tag()
def get_beian_url():
    return settings.BEIAN_URL


@register.simple_tag()
def get_beian_text():
    return settings.BEIAN_TEXT


@register.simple_tag(takes_context=True)
def get_file_url(context, file_id):
    return reverse(
        'funfile:get_file',
        kwargs={"file_id": file_id}
    )


@register.simple_tag
def get_site_gray():
    return settings.SITE_GRAY


@register.simple_tag
def get_allow_registration():
    return settings.ALLOWED_REGISTRATION


@register.simple_tag
def get_site_name():
    return settings.SITE_NAME
