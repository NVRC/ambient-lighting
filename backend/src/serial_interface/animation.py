from collections import deque
from enum import Enum
from datetime import timedelta

from pydantic import BaseModel

from models import CommandGenerator, Strip
from serial_interface import commands

AnimationType = Enum("AnimationType", ["SHIFT"])


class AnimationSettings(BaseModel):
    """AnimationSettings encapsulates wire safe information to animation a lighting strip."""

    rate: timedelta
    animation_type: AnimationType


class ShiftAnimation(AnimationSettings):
    """ShiftAnimation encapsulates settings for a shifting animation."""

    shift_by: int


def shift_generator(strip: Strip, settings: ShiftAnimation) -> CommandGenerator:
    """shift_generator returns an iterator yielding a CommandList.

    Assumes LedMap.keys() is a continuous integer array where 0 <= index < Strip.number_of_leds.
    """
    leds = deque()
    for i in range(0, strip.number_of_leds):
        leds.append(strip.leds[i])
    while True:
        cmds = commands.set_strip(leds)
        yield cmds
        leds.rotate(settings.shift_by)

    # step: int = 0
    # led_deque = deque(led_map)
    # initial_index = step * settings.shift_by
    # for i in range(0, NUM_LEDS):

    # wrap_around_index = max(led_map.keys()) - settings.shift_by

    # for index, led in led_map.items():
    #     if index >= wrap_around_index:
    #         new_led_map[index - wrap_around_index] = led
    #     else:
    #         new_led_map[wrap_around_index - index] = led
    # for index, led in wrap_around_index =
