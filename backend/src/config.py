from typing import Optional
from pydantic import BaseModel, BaseSettings, Field

DEV_LABEL = "DEV"
PROD_LABEL = "PROD"


class AppConfig(BaseModel):
    description: str = "Interfaces over serial to control ambient lights."


class GlobalConfig(BaseSettings):
    app_config: AppConfig = AppConfig()
    serial_device_path: Optional[str] = Field(default=None, env="serial_device_path")
    debug: bool = False


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
            return DevConfig(_env_file=".env", serial_device_path="/dev/ttyUSB0")
        if env_label == PROD_LABEL:
            return ProdConfig(_env_file=".env")
        raise Exception("Invalid environment label '{}' provided".format(env_label))
