from enum import Enum


class FileUploadStrategy(Enum):
    STANDARD = "standard"
    DIRECT = "direct"


class FileUploadStorage(Enum):
    AZURE = "az"
    LOCAL = "local"
