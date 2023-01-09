from dataclasses import dataclass
from typing import Dict, NamedTuple

class RGB(NamedTuple):
  red: int
  green: int
  blue: int

class Led(NamedTuple):
  index: int
  color: RGB

@dataclass
class Strip:
  id: 1
  leds: Dict[int, Led]