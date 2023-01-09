import argparse
from typing import Union, List

from fastapi import FastAPI, Request
from loguru import logger

from models import Led, Strip, RGB
import serialInterface.commands as commands
from config import (
  DEV_LABEL,
  ConfigFactory
)

from state import AppState

NUM_LEDS = 60

if __name__ == "__main__":
  import uvicorn

  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument("--serial-device", dest="serial_device", required=True)
  args = arg_parser.parse_args()

  app = FastAPI()

  config = ConfigFactory(args.serial_device, DEV_LABEL)
  # Initialize state from configuration
  app.state = AppState(config)

  @app.get("/strips/{strip_id}", response_model=Strip)
  def read_strip(request: Request, strip_id: int) -> Strip:
    return request.app.state.strip

  @app.post("/strips/{strip_id}/leds", response_model=List[Led])
  def post_strip_leds(request: Request, strip_id: int, leds: List[Led]) -> List[Led]:
    link = request.app.state.link

    # Update state
    request.app.state.strips.get(strip_id).leds = leds
    commands.process(link, commands.set_show_on_write(False))
    for led in leds:
      ok = commands.process(link, commands.set_led(led))
      if not ok:
        return False
    commands.process(link, commands.set_show_on_write(True))
    return leds

  @app.get("/strips/{strip_id}/leds/{led_id}", response_model=Led)
  def read_led(request: Request, strip_id: int, led_id: int) -> Union[Led, None]:
    return request.app.state.strips.get(strip_id).leds.get(led_id, None)

  @app.post("/strips/{strip_id}/leds/{led_id}")
  def post_led(request: Request, strip_id: int, led_id: int, led: Led) -> Union[Led, None]:
    strip = request.app.state.strips.get(strip_id)
    link = request.app.state.link
    curr_led = strip.leds.get(led_id, None)
    if curr_led is None:
      return None
    strip.leds[led_id] = led
    return commands.process(link, commands.set_led(led))

  uvicorn.run(
    "__main__:app",
    log_level="debug",
  )