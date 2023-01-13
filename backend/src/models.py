"""This module defines pydantic class models.
"""

from typing import List, Iterator, MutableMapping
from pydantic import BaseModel

NUM_LEDS = 60

Command = List  # TODO: restrict shape with pydantic
CommandList = List[Command]
CommandGenerator = Iterator[List[Command]]


class RGB(BaseModel):
    """RGB color model."""

    red: int
    green: int
    blue: int

    def __eq__(self, other: "RGB"):
        if not isinstance(self, other.__class__):
            return NotImplementedError
        return (
            (self.red == other.red)
            & (self.green == other.green)
            & (self.blue == other.blue)
        )


class Led(BaseModel):
    """Led modeling an index within a Strip and a color."""

    color: RGB


LedMap = MutableMapping[int, Led]


class Strip(BaseModel):
    """An ambient light strip containing a map of Leds."""

    id: int
    brightness: int
    number_of_leds: int
    leds: LedMap
