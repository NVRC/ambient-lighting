import argparse
from typing import Union, List
import time

from fastapi import FastAPI
from loguru import logger

from pySerialTransfer import pySerialTransfer as txfer

from models import Led, Strip
import serial.commands as commands

if __name__ == "__main__":

  arg_parser = argparse.ArgumentParser(description="Interfaces over serial to control ambient lights.")
  arg_parser.add_argument("--serial-device", dest="serial_device", required=True)
  args = arg_parser.parse_args()

  try:
    link = txfer.SerialTransfer(args.serial_device, debug=True)
  except txfer.InvalidSerialPort as e:
    raise e
  finally:
    link.open()

  app = FastAPI()

  strip = Strip()

  @app.get("/strips/{strip_id}")
  def read_strip(strip_id: int) -> Strip:
    return strip

  @app.post("/strips/{strip_id}/leds")
  def post_strip_leds(strip_id: int, leds: List[Led]) -> bool:
    strip.leds = leds
    commands.process(link, commands.set_show_on_write(False))
    for led in leds:
      commands.process(link, commands.set_led())
    return True

  @app.get("/strips/{strip_id}/leds/{led_id}")
  def read_led(strip_index: int, led_index: int) -> Union[Led, None]:
    return strip.leds.get(led_index, None)

  @app.post("/strips/{strip_id}/leds/{led_id}")
  def post_led(strip_index: int, led_index: int) -> bool:
    led = strip.leds.get(led_index, None)
    if led is None:
      return False
    strip.leds[led_index] = led
    return True
