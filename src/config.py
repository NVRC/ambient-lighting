from typing import Optional
from pydantic import BaseModel, BaseSettings, Field

DEV_LABEL = "DEV"
PROD_LABEL = "PROD"

class AppConfig(BaseModel):
  description: str = "Interfaces over serial to control ambient lights."

class GlobalConfig(BaseSettings):
  app_config: AppConfig = AppConfig()
  serial_device_path: str
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
  def __init__(self, serial_device_path: str, env_label: Optional[str]):
    self.env_label = env_label
    self.serial_device_path = serial_device_path

  def __call__(self):
    if self.env_label == "dev":
      return DevConfig(serial_device_path=self.serial_device_path)
    elif self.env_label == ProdConfig.title:
      return ProdConfig(serial_device_path=self.serial_device_path)
    else:
      raise Exception("Invalid environment label '{}' provided".format(self.env_label))