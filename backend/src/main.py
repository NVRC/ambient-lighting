import argparse
from typing import Union, List

from fastapi import FastAPI, Request

from models import Led, Strip, LedMap
from serial_interface import commands
from config import DEV_LABEL, ConfigFactory

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
    def read_strip(request: Request, strip_id: int) -> Union[Strip, None]:
        return request.app.state.strips.get(strip_id, None)

    @app.post("/strips/{strip_id}/leds", response_model=LedMap)
    def post_strip_leds(request: Request, strip_id: int, led_map: LedMap) -> List[Led]:
        link = request.app.state.link

        # Update state
        request.app.state.strips.get(strip_id).leds = led_map
        commands.process(link, commands.set_show_on_write(False))
        for index, led in led_map:
            processed = commands.process(link, commands.set_led(index, led))
            if not processed:
                return False
        commands.process(link, commands.set_show_on_write(True))
        return led_map

    @app.get("/strips/{strip_id}/leds/{index_id}", response_model=Led)
    def read_led(request: Request, strip_id: int, index_id: int) -> Union[Led, None]:
        return request.app.state.strips.get(strip_id).leds.get(index_id, None)

    @app.post("/strips/{strip_id}/leds/{index_id}")
    def post_led(
        request: Request, strip_id: int, index_id: int, led: Led
    ) -> Union[Led, None]:
        strip = request.app.state.strips.get(strip_id)
        link = request.app.state.link
        curr_led = strip.leds.get(index_id, None)
        if curr_led is None:
            return None
        strip.leds[index_id] = led
        return commands.process(link, commands.set_led(index_id, led))

    uvicorn.run(
        "__main__:app",
        log_level="debug",
    )
