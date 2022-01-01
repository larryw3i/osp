
import bleach
from django.conf import settings

# COMMON
create_html = '_create.html'
detail_html = '_detail.html'
delete_html = '_delete.html'
update_html = '_update.html'
list_html = '_list.html'
default_uuid = 'db3f0b38-27d9-11ea-b421-57517fb382fd'


def bleach_clean(content):
    return bleach.clean(
        content,
        tags=settings.BLEACH_TAGS,
        attributes=settings.BLEACH_ATTRIBUTES,
        styles=settings.BLEACH_STYLES)
