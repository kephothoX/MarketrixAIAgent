import os
from dotenv import load_dotenv

load_dotenv()


from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    YamlConfigSettingsSource,
    PydanticBaseSettingsSource,
)
from typing import Type, Tuple


class Settings(BaseSettings):
    gcloud_location: str = os.environ.get("LOCATION") or "us-central1"
    gcloud_project_id: str = (
        os.environ.get("GOOGLE_CLOUD_PROJECT_ID") or "marketrix-agent"
    )
    backend_url: str = os.environ.get("BACKEND_URL") or "http://127.0.0.1:8080"
    storage_bucket_name: str = (
        os.environ.get("STORAGE_BUCKET_NAME") or "marketrix_agent_storage"
    )

    model_config = SettingsConfigDict(
        yaml_file="settings.yaml", yaml_file_encoding="utf-8"
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        """Customize the settings sources and their priority order.

        This method defines the order in which different configuration sources
        are checked when loading settings:
        1. Environment variables
        2. YAML configuration file
        3. Constructor-provided values

        Args:
            settings_cls: The Settings class type.
            init_settings: Settings from class initialization.
            env_settings: Settings from environment variables.
            dotenv_settings: Settings from .env file (not used).
            file_secret_settings: Settings from secrets file (not used).

        Returns:
            A tuple of configuration sources in priority order.
        """
        return (
            env_settings,  # Environment variables as first priority
            YamlConfigSettingsSource(
                settings_cls
            ),  # YAML configuration file as second priority
            init_settings,  # Constructor-provided values as last priority
        )


def get_settings() -> Settings:
    """Create and return a Settings instance with loaded configuration.

    Initializes a Settings object that loads configuration values from
    environment variables and the YAML configuration file, with environment
    variables taking precedence.

    Returns:
        A fully configured Settings instance containing all application configuration.
    """
    return Settings()
