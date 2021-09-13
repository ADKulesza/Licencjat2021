from django.conf import settings
from django.core.files.storage import FileSystemStorage

class EEGLABfilesStorage(FileSystemStorage):
    def __init__(self, options=None):
        if not options:
            options = settings.EEGLAB_FILES_STORAGE_OPTIONS

    def _save(self, name, content):
        if self.exists(name):
            self.delete(name)
        return super(FileSystemStorage, self)._save(name, content)