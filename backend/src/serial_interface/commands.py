from models import Led, LedMap, Command, CommandList

# An index < 0 denotes an action event.
#  action_key |  action
#      -1     |  clear strip
#      -2     |  set brightness, read from [1]
#      -3     |  set show on write, where false <= 0 < true


def set_strip(led_map: LedMap) -> CommandList:
    cmds = [set_show_on_write(False)]
    length = len(led_map)
    for index in range(0, length):
        led = led_map[index]
        if index == length - 1:
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
