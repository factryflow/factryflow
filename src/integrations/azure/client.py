from dataclasses import dataclass
from functools import lru_cache

from common.utils.services import assert_settings
from storages.backends.azure_storage import AzureStorage


# TODO: Add other essential Azure Storage Configuration (i.e. AZURE_CONNECTION_STRING, AZURE_OBJECT_PARAMETERS)
@dataclass
class AZStorageConfig:
    """
    Azure Storage Configuration.
    """

    AZURE_ACCOUNT_NAME: str
    AZURE_ACCOUNT_KEY: str
    AZURE_CONTAINER: str


@lru_cache
def az_storage_get_credentials() -> AZStorageConfig:
    required_config = assert_settings(
        [
            "AZURE_ACCOUNT_NAME",
            "AZURE_ACCOUNT_KEY",
            "AZURE_CONTAINER",
        ],
        error_message_prefix="Azure Storage is not configured properly.",
    )

    return AZStorageConfig(
        AZURE_ACCOUNT_NAME=required_config["AZURE_ACCOUNT_NAME"],
        AZURE_ACCOUNT_KEY=required_config["AZURE_ACCOUNT_KEY"],
        AZURE_CONTAINER=required_config["AZURE_CONTAINER"],
    )


def az_storage_get_client():
    credentials = az_storage_get_credentials()

    return AzureStorage(
        account_name=credentials.AZURE_ACCOUNT_NAME,
        account_key=credentials.AZURE_ACCOUNT_KEY,
        azure_container=credentials.AZURE_CONTAINER,
    )


# TODO: Building Azure Storage Presigned POST URL functionality
def az_storage_generate_presigned_post_url():
    pass
