from collections import deque
from enum import Enum
from datetime import timedelta

from typing import Callable, Dict, List

from pydantic import BaseModel

from models import CommandGenerator, Strip, RGB
from serial_interface import commands


class AnimationType(Enum):
    SHIFT = "SHIFT"
    GRADIENT_POLYLINEAR_INTERPOLATION = "GRADIENT_POLYLINEAR_INTERPOLATION"


class AnimationSettings(BaseModel):
    """AnimationSettings encapsulates generic wire safe animation settings."""

    rate: timedelta


class ShiftAnimation(AnimationSettings):
    """ShiftAnimation encapsulates settings for a shifting animation."""

    shift_by: int


class RandGradient2DLinearInterpolation(AnimationSettings):
    """RandGradient2DLinearInterpolation encapsulates polylinear gradient settings."""

    colors: List[RGB]
    y_len: int


class AnimationDetails(BaseModel):
    """Animation encapsulates wire safe information to inflate
    user settings for a specific animation.
    """

    animation_type: AnimationType
    settings: dict  # Use dict instead of AnimationSettings for JS compat

    def __hash__(self) -> int:
        return hash(self.animation_type)


AnimationGeneratorPrototype = Callable[
    [Strip, RandGradient2DLinearInterpolation], CommandGenerator
]

AnimationFunctionRegistry: Dict[AnimationDetails, AnimationGeneratorPrototype] = {}


def register_animation(
    animation_details: AnimationDetails,
):
    """Register a function as an animation."""

    def decorator(function):
        AnimationFunctionRegistry[animation_details] = function

        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)

        return wrapper

    return decorator


def linear_gradient(start: RGB, end: RGB, steps: int) -> List[RGB]:
    """Returns a linear gradient between two colors."""
    output_colors = [start]
    for step in range(1, steps):
        rgb = RGB(
            red=int(
                start["red"] + (float(step) / (steps - 1)) * (end["red"] - start["red"])
            ),
            blue=int(
                start["blue"]
                + (float(step) / (steps - 1)) * (end["blue"] - start["blue"])
            ),
            green=int(
                start["green"]
                + (float(step) / (steps - 1)) * (end["red"] - start["green"])
            ),
        )
        output_colors.append(rgb)
    return output_colors


def polylinear_gradient(colors: List[RGB], steps: int) -> List[RGB]:
    """Returns a polylinear gradient between two colors."""
    len_colors = len(colors)
    sub_length = int(float(steps) / (len_colors - 1))

    t_colors = []
    for z_index in range(0, len_colors - 1):
        start = colors[z_index]
        end = colors[z_index + 1]
        sub_l = linear_gradient(start, end, sub_length)
        t_colors.extend(sub_l)
    return t_colors


@register_animation(
    animation_details=AnimationDetails(
        animation_type=AnimationType.SHIFT,
        settings=ShiftAnimation(rate=timedelta(seconds=5), shift_by=1),
    )
)
def shift_generator(strip: Strip, settings: ShiftAnimation) -> CommandGenerator:
    """Returns an iterator yielding a CommandList.

    Assumes LedMap.keys() is a continuous integer array where 0 <= index < Strip.number_of_leds.
    """
    leds = deque()
    for i in range(0, strip.number_of_leds):
        leds.append(strip.leds[i])
    while True:
        cmds = commands.set_strip(leds)
        yield cmds
        leds.rotate(settings.get("shift_by"))


@register_animation(
    animation_details=AnimationDetails(
        animation_type=AnimationType.GRADIENT_POLYLINEAR_INTERPOLATION,
        settings=RandGradient2DLinearInterpolation(
            rate=timedelta(seconds=1),
            colors=[RGB(red=0, green=255, blue=0), RGB(red=0, green=0, blue=255)],
            y_len=25,
        ),
    )
)
def rand_gradient_polylinear_interpolation_generator(
    strip: Strip, settings: RandGradient2DLinearInterpolation
) -> CommandGenerator:
    """Generates a polylinear interpolated sequence."""

    gradient = polylinear_gradient(settings.get("colors"), settings.get("y_len"))

    moving_index = 0
    direction_left = True
    # Translates back and forth to animate leds.

    while True:
        color = gradient[moving_index]
        cmds = commands.set_color(color, strip.number_of_leds - 1)
        yield cmds
        if moving_index >= settings.get("y_len") - 1:
            direction_left = False
        if moving_index <= 0:
            direction_left = True
        if direction_left:
            moving_index = moving_index + 1
        else:
            moving_index = moving_index - 1
