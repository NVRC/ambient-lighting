from fastapi.datastructures import State
from config import GlobalConfig
import serialInterface.commands as commands

from models import Led, RGB, Strip

class AppState(State):
  def __init__(self, config: GlobalConfig):
    leds = {}
    for i in range(0, 60):
      rgb = RGB(red=255, green=255, blue=255)
      leds[i] = Led(index=i, color=rgb)
    state = {
      "link": commands.init_link(config.serial_device_path),
      "strips": {
        1: Strip(leds=leds)
      },
    }
    super().__init__(state)