import os

from common.enums import FileUploadStorage, FileUploadStrategy

from .components.common import BASE_DIR
from .components.env import env_to_enum

FILE_UPLOAD_STRATEGY = env_to_enum(
    FileUploadStrategy, os.getenv("FILE_UPLOAD_STRATEGY", default="direct")
)
FILE_UPLOAD_STORAGE = env_to_enum(
    FileUploadStorage, os.getenv("FILE_UPLOAD_STORAGE", default="az")
)

if FILE_UPLOAD_STORAGE == FileUploadStorage.LOCAL:
    MEDIA_ROOT_NAME = "media"
    MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_ROOT_NAME)
    MEDIA_URL = f"/{MEDIA_ROOT_NAME}/"

if FILE_UPLOAD_STORAGE == FileUploadStorage.AZURE:
    # Using django-storages
    # https://django-storages.readthedocs.io/en/1.13.2/backends/azure.html
    DEFAULT_FILE_STORAGE = "backend.custom_azure.AzureMediaStorage"

    AZURE_ACCOUNT_NAME = os.getenv("AZURE_ACCOUNT_NAME")
    AZURE_ACCOUNT_KEY = os.getenv("AZURE_ACCOUNT_KEY")
    AZURE_CONTAINER = os.getenv("AZURE_ACCOUNT_CONTAINER")

    _AZURE_STORAGE_CUSTOM_DOMAIN = os.getenv("AZURE_STORAGE_CUSTOM_DOMAIN", default="")

    if _AZURE_STORAGE_CUSTOM_DOMAIN:
        AZURE_CUSTOM_DOMAIN = f"{AZURE_ACCOUNT_NAME}.blob.core.windows.net"
        MEDIA_URL = f"https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/"
