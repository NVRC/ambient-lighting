import argparse

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import Led, Strip, LedMap
from serial_interface import commands
from config import DEV_LABEL, ConfigFactory

from state import AppState


origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:19006",
    "http://127.0.0.1:19006",
]

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

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["POST", "GET"],
        allow_headers=["*"],
    )

    @app.get("/strips/{strip_id}", response_model=Strip)
    def read_strip(request: Request, strip_id: int) -> Strip:
        strip = request.app.state.strips.get(strip_id, None)
        if strip is None:
            raise HTTPException(status_code=404, detail="Lighting strip not found")
        return strip

    @app.post("/strips/{strip_id}/leds", status_code=201)
    def post_strip_leds(request: Request, strip_id: int, led_map: LedMap):
        link = request.app.state.link
        commands.process(link, commands.set_show_on_write(False))
        for index in led_map.keys():
            led = led_map[index]
            commands.process(link, commands.set_led(index, led))
        commands.process(link, commands.set_show_on_write(True))
        request.app.state.strips.get(strip_id).leds = led_map

    @app.get("/strips/{strip_id}/leds/{index_id}")
    def read_led(request: Request, strip_id: int, index_id: int) -> Led:
        strip = request.app.state.strips.get(strip_id, None)
        if strip is None:
            raise HTTPException(status_code=404, detail="Lighting strip not found")
        led = strip.leds.get(index_id, None)
        if led is None:
            raise HTTPException(status_code=404, detail="Led not found")
        return led

    @app.post("/strips/{strip_id}/leds/{index_id}", status_code=201)
    def post_led(request: Request, strip_id: int, index_id: int, led: Led):
        strip = request.app.state.strips.get(strip_id)
        link = request.app.state.link

        strip.leds[index_id] = led
        commands.process(link, commands.set_led(index_id, led))

    uvicorn.run(
        "__main__:app",
        log_level="debug",
    )
