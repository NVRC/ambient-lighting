from typing import Optional
from pydantic import BaseModel, BaseSettings

DEV_LABEL = "DEV"
PROD_LABEL = "PROD"


class AppConfig(BaseModel):
    description: str = "Interfaces over serial to control ambient lights."


class GlobalConfig(BaseSettings):
    app_config: AppConfig = AppConfig()
    serial_device_path: Optional[str] = None
    debug: bool = False

    class Config:
        env_file: str = ".env"


class DevConfig(GlobalConfig):
    title: str = DEV_LABEL
    debug: bool = True


class ProdConfig(GlobalConfig):
    title: str = PROD_LABEL
    debug: bool = False


class ConfigFactory:
    """ConfigFactory returns an environment specific configuration."""

    def __call__(self, env_label: Optional[str]):
        if env_label == DEV_LABEL:
            return DevConfig()
        if env_label == PROD_LABEL:
            return ProdConfig()
        raise Exception("Invalid environment label '{}' provided".format(env_label))
