"""This module defines pydantic class models.
"""

from typing import Dict
from pydantic import BaseModel


class RGB(BaseModel):
    """RGB color model."""

    red: int
    green: int
    blue: int


class Led(BaseModel):
    """Led modeling an index within a Strip and a color."""

    color: RGB


LedMap = Dict[int, Led]


class Strip(BaseModel):
    """An ambient light strip containing a map of Leds."""

    id: int = 1
    brightness: int = 255
    leds: LedMap
