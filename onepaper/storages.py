from django.conf import os
from storages.backends.s3boto3 import S3Boto3Storage

__all__ = (
    "S3StaticStorage",
    "S3DefaultStorage",
)

# for media
class S3DefaultStorage(S3Boto3Storage):
    default_acl = "public-read"
    location = "media"
    file_overwrite = False


# for static
class S3StaticStorage(S3Boto3Storage):
    default_acl = "public-read"
    GREEN = os.environ.get("GREEN", "True") != "False"
    if GREEN:
        location = "static-green"
    else:
        location = "static"
