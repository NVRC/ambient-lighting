"""This module encapsulates application state.
"""
from typing import List

from fastapi.datastructures import State
from config import GlobalConfig
from serial_interface import commands, controller, animation

from models import Led, RGB, Strip, LedMap, NUM_LEDS


class AppState(State):
    """Subclasses State and inflates from GlobalConfig.

    Controls
    """

    def __init__(self, config: GlobalConfig):
        leds: LedMap = {}
        for i in range(0, 60):
            rgb = RGB(red=255, green=255, blue=255)
            leds[i] = Led(index=i, color=rgb)
        state = {
            "strips": {
                1: Strip(number_of_leds=NUM_LEDS, leds=leds, id=1, brightness=255)
            }
        }
        if config.serial_device_path is None:
            state["serial_link_available"] = False
        else:
            state["serial_link_available"] = True
            state["link"] = controller.Controller(config.serial_device_path)

        super().__init__(state)

    def command(self, cmds: List[commands.Command]):
        if self.serial_link_available:
            self.link.process(cmds)

    def animate(self, strip: Strip, settings: animation.AnimationSettings):
        if self.serial_link_available:
            self.link.animate(strip, settings)
