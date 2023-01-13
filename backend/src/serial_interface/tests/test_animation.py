from datetime import timedelta
from models import Led, LedMap, RGB, Strip
from serial_interface.animation import shift_generator, ShiftAnimation, AnimationType
from serial_interface import commands

t_led_m: LedMap = {
    0: Led(color=RGB(red=0, green=0, blue=0)),
    1: Led(color=RGB(red=1, green=1, blue=1)),
    2: Led(color=RGB(red=2, green=2, blue=2)),
}
t_strip = Strip(id=1, brightness=255, number_of_leds=3, leds=t_led_m)
t_cmds = commands.set_strip(t_strip.leds)


def test_shift_generator():
    exp_led_m: LedMap = {
        0: Led(color=RGB(red=2, green=2, blue=2)),
        1: Led(color=RGB(red=0, green=0, blue=0)),
        2: Led(color=RGB(red=1, green=1, blue=1)),
    }
    exp_cmds = commands.set_strip(exp_led_m)
    settings = ShiftAnimation(
        rate=timedelta(minutes=1), animation_type=AnimationType.SHIFT, shift_by=1
    )
    generator = shift_generator(t_strip, settings)
    initial_iter_cmds = next(generator)
    assert initial_iter_cmds == t_cmds
    next_iter_cmds = next(generator)
    assert next_iter_cmds == exp_cmds
