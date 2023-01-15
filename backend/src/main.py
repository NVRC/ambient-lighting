from typing import List

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import Led, Strip, LedMap
from serial_interface import commands, animation
from config import DEV_LABEL, ConfigFactory

from state import AppState


origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:19006",
    "http://127.0.0.1:19006",
]


if __name__ == "__main__":
    import uvicorn

    app = FastAPI()

    configFactory = ConfigFactory()
    # Initialize state from configuration
    app.state = AppState(configFactory(DEV_LABEL))

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["POST", "GET"],
        allow_headers=["*"],
    )

    @app.get("/strips/{strip_id}", response_model=Strip, tags=["strips"])
    def read_strip(request: Request, strip_id: int) -> Strip:
        strip = request.app.state.strips.get(strip_id, None)
        if strip is None:
            raise HTTPException(status_code=404, detail="Lighting strip not found")
        return strip

    @app.post("/strips/{strip_id}", status_code=201, tags=["strips"])
    def post_strip(request: Request, strip_id: int, strip: Strip) -> Strip:
        curr_strip = request.app.state.strips.get(strip_id, None)
        if curr_strip is None:
            raise HTTPException(status_code=404, detail="Lighting strip not found")

        request.app.state.strips[strip_id] = strip

        cmds = [commands.set_brightness(strip.brightness)]
        cmds.extend(commands.set_strip(strip.leds))
        request.app.state.command(cmds)
        return strip

    @app.post("/strips/{strip_id}/animate", status_code=200, tags=["strips"])
    def post_strip_animation(
        request: Request, strip_id: int, animation_details: animation.AnimationDetails
    ) -> animation.AnimationDetails:
        curr_strip = request.app.state.strips.get(strip_id, None)
        if curr_strip is None:
            raise HTTPException(status_code=404, detail="Lighting strip not found")

        request.app.state.animate(curr_strip, animation_details)

    @app.get("/strips/{strip_id}/animate", status_code=200, tags=["strips"])
    def get_strip_animations(
        request: Request, strip_id: int
    ) -> List[animation.AnimationDetails]:
        curr_strip = request.app.state.strips.get(strip_id, None)
        if curr_strip is None:
            raise HTTPException(status_code=404, detail="Lighting strip not found")

        return list(animation.AnimationFunctionRegistry.keys())

    @app.post("/strips/{strip_id}/leds", status_code=201, tags=["strips", "leds"])
    def post_strip_leds(request: Request, strip_id: int, led_map: LedMap) -> LedMap:
        cmds = commands.set_strip(led_map)
        request.app.state.command(cmds)

        request.app.state.strips.get(strip_id).leds = led_map
        return led_map

    @app.get("/strips/{strip_id}/leds/{index_id}", tags=["strips", "leds"])
    def read_led(request: Request, strip_id: int, index_id: int) -> Led:
        strip = request.app.state.strips.get(strip_id, None)
        if strip is None:
            raise HTTPException(status_code=404, detail="Lighting strip not found")
        led = strip.leds.get(index_id, None)
        if led is None:
            raise HTTPException(status_code=404, detail="Led not found")
        return led

    @app.post(
        "/strips/{strip_id}/leds/{index_id}", status_code=201, tags=["strips", "leds"]
    )
    def post_led(request: Request, strip_id: int, index_id: int, led: Led) -> Led:
        strip = request.app.state.strips.get(strip_id)
        request.app.state.command([commands.set_led(index_id, led)])

        strip.leds[index_id] = led
        return led

    uvicorn.run(
        "__main__:app",
        log_level="debug",
    )
