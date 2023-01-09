from typing import Dict
from pydantic import BaseModel

class RGB(BaseModel):
  red: int
  green: int
  blue: int

class Led(BaseModel):
  index: int
  color: RGB

class Strip(BaseModel):
  id: int = 1
  leds: Dict[int, Led]