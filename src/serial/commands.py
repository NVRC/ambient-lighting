from typing import List

from loguru import logger
from pySerialTransfer import pySerialTransfer

from models import Led

Command = List

def clear_strip() -> Command:
  return [-1, 0, 0, 0]

def set_brightness(brightness: int) -> Command:
  return [-2, brightness, 0, 0]

def set_led(led: Led) -> Command:
  return [Led.index, Led.red, Led.green, Led.blue]

def set_show_on_write(show_on_write: bool) -> Command:
  show_on_write_int = 0
  if show_on_write:
    show_on_write_int = 1
  return [-3, show_on_write_int, 0, 0]


def process(link: pySerialTransfer, cmd: Command) -> bool:
  """Process a cmd over the provided link. """
  try:
    sendSize = 0
    sendSize = link.tx_obj(cmd, start_pos=sendSize, byte_format='<')
    logger.debug("Sending: ", cmd, sendSize)
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
    availableBytes = link.available()
    rec = link.rx_obj(obj_type=(list), byte_format='<', list_format='i', obj_byte_size=sendSize)
    if rec is None:
      raise Exception("Serial receive failed")
    logger.debug("Bytes read: ", availableBytes, "Received: ", rec, type(rec), repr(rec))
  except Exception as e:
    logger.error("Failed to process {} on link {}: {}", cmd, link, e)