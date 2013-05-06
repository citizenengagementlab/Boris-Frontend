from django.conf import settings
from django.contrib.staticfiles.storage import CachedFilesMixin
from storages.backends.s3boto import S3BotoStorage

class CachedStaticS3BotoStorage(CachedFilesMixin, S3BotoStorage):
	pass

class StaticRootS3BotoStorage(CachedStaticS3BotoStorage):
    """
    Storage for static files.
    """

    def __init__(self, *args, **kwargs):
        kwargs['location'] = 'static'
        super(CachedStaticS3BotoStorage, self).__init__(*args, **kwargs)

class MediaRootS3BotoStorage(CachedStaticS3BotoStorage):
    """
    Storage for uploaded media files.
    """

    def __init__(self, *args, **kwargs):
        kwargs['location'] = 'media'
        super(CachedStaticS3BotoStorage, self).__init__(*args, **kwargs)