from typing import List

from loguru import logger
from pySerialTransfer import pySerialTransfer

from models import Led

Command = List # TODO: restrict shape with pydantic

# An index < 0 denotes an action event.
#  action_key |  action
#      -1     |  clear strip
#      -2     |  set brightness, read from [1]
#      -3     |  set show on write, where false <= 0 < true

def clear_strip() -> Command:
  """Returns a Command to clear the strip."""
  return [-1, 0, 0, 0]

def set_brightness(brightness: int) -> Command:
  """Returns a Command to set the brightness of the strip."""
  #TODO: Strip refactor
  return [-2, brightness, 0, 0]

def set_led(led: Led) -> Command:
  """Returns a Command to set an Led."""
  return [led.index, led.color.red, led.color.green, led.color.blue]

def set_show_on_write(show_on_write: bool) -> Command:
  """Returns a Command to set showOnWrite."""
  show_on_write_int = 0
  if show_on_write:
    show_on_write_int = 1
  return [-3, show_on_write_int, 0, 0]

def process(link: pySerialTransfer, cmd: Command) -> bool:
  """Process a cmd over the provided link. """
  try:
    sendSize = link.tx_obj(cmd, start_pos=0, byte_format='<')
    logger.debug("sending command {} of {} bytes.", cmd, sendSize)
    if sendSize is None:
      raise Exception("Serial transaction failed: {}".format(sendSize))

    link.send(sendSize)
    ###################################################################
    # Wait for a response and report any errors while receiving packets
    ###################################################################
    while not link.available():
      if link.status < 0:
        if link.status == pySerialTransfer.CRC_ERROR:
            logger.error('ERROR: CRC_ERROR')
        elif link.status == pySerialTransfer.PAYLOAD_ERROR:
            logger.error('ERROR: PAYLOAD_ERROR')
        elif link.status == pySerialTransfer.STOP_BYTE_ERROR:
            logger.error('ERROR: STOP_BYTE_ERROR')
        else:
            logger.error('ERROR: link status {}'.format(link.status))

    ###################################################################
    # Parse response
    ###################################################################
    rec = link.rx_obj(obj_type=(list), byte_format='<', list_format='i', obj_byte_size=sendSize)
    if rec is None:
      raise Exception("Serial receive failed")
    logger.debug("received {} of length {} bytes.", rec, sendSize)
  except Exception as e:
    logger.error("Failed to process {} on link {}: {}", cmd, link, e)

def init_link(serial_device: str) -> pySerialTransfer:
  try:
    link = pySerialTransfer.SerialTransfer(serial_device, debug=True)
  except pySerialTransfer.InvalidSerialPort as e:
    raise e
  finally:
    link.open()
  return link