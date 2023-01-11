from typing import List


from models import Led, LedMap

Command = List  # TODO: restrict shape with pydantic

NUM_LEDS = 60

# An index < 0 denotes an action event.
#  action_key |  action
#      -1     |  clear strip
#      -2     |  set brightness, read from [1]
#      -3     |  set show on write, where false <= 0 < true


def set_strip(led_map: LedMap) -> List[Command]:
    cmds = [set_show_on_write(False)]
    for index in led_map:  # pylint: disable=consider-using-dict-items
        led = led_map[index]
        if index == NUM_LEDS - 1:
            cmds.append(set_show_on_write(True))
        cmds.append(set_led(index, led))
    return cmds


def clear_strip() -> Command:
    """Returns a Command to clear the strip."""
    return [-1, 0, 0, 0]


def set_brightness(brightness: int) -> Command:
    """Returns a Command to set the brightness of the strip."""
    # TODO: Strip refactor
    return [-2, brightness, 0, 0]


def set_led(index: int, led: Led) -> Command:
    """Returns a Command to set an Led."""
    return [index, led.color.red, led.color.green, led.color.blue]


def set_show_on_write(show_on_write: bool) -> Command:
    """Returns a Command to set showOnWrite."""
    show_on_write_int = 0
    if show_on_write:
        show_on_write_int = 1
    return [-3, show_on_write_int, 0, 0]
