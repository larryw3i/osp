
import hashlib
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage


def upload_to(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class FunFileStorage(FileSystemStorage):
    def _save(self, name, content):
        sha256 = hashlib.sha256()
        for chunk in content.chunks():
            sha256.update(chunk)
        name = sha256.hexdigest()
        full_path = super().path(name)
        if(os.path.exists(full_path)):
            return name
        return super()._save(name, content)
