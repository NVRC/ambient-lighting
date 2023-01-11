"""This module encapsulates application state.
"""
from typing import List

from threading import Lock

from fastapi.datastructures import State
from config import GlobalConfig
from serial_interface import commands

from models import Led, RGB, Strip, LedMap


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
            "link": commands.init_link(config.serial_device_path),
            "strips": {1: Strip(leds=leds)},
            "link_lock": Lock(),
        }
        super().__init__(state)

    def command(self, cmds: List[commands.Command]):
        with self.link_lock:
            for command in cmds:
                commands.process(self.link, command)
