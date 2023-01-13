from typing import List
from threading import Lock

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from pySerialTransfer import pySerialTransfer
from loguru import logger

from models import Strip


from serial_interface.animation import AnimationSettings, AnimationType, shift_generator

EXECUTOR_ANIMATION_NAME = "animation"


class Controller:
    def __init__(self, serial_device: str):
        """Initialize a serial interface.

        Raises:
            InvalidSerialPort
        """
        try:
            link = pySerialTransfer.SerialTransfer(serial_device, debug=True)
        except pySerialTransfer.InvalidSerialPort as ex:
            raise ex
        self.link = link
        self._link_lock = Lock()

        self.apscheduler = BackgroundScheduler(
            executors={EXECUTOR_ANIMATION_NAME: ThreadPoolExecutor()},
            job_defaults={"max_instances": 1, "coalesce": False},
        )

        self.link.open()

    def process(self, *cmds: List) -> bool:
        with self._link_lock:
            for cmd in cmds:
                _process(self.link, cmd)

    def animate(self, strip: Strip, animation_settings: AnimationSettings) -> bool:
        if animation_settings.animation_type == AnimationType.SHIFT:
            generator = shift_generator(strip, settings=animation_settings)
        else:
            return False

        def _job():
            cmds = next(generator)
            with self._link_lock:
                for cmd in cmds:
                    _process(self.link, cmd)

        _job()
        self.apscheduler.add_job(
            _job, "interval", int(animation_settings.rate.total_seconds())
        )
        return True


def _process(link: pySerialTransfer, cmd: List) -> bool:
    """Process a cmd over the provided link."""
    send_size = link.tx_obj(cmd, start_pos=0, byte_format="<")
    logger.debug("sending command {} of {} bytes.", cmd, send_size)
    if send_size is None:
        raise Exception("Serial transaction failed: {}".format(send_size))

    link.send(send_size)
    ###################################################################
    # Wait for a response and report any errors while receiving packets
    ###################################################################
    while not link.available():
        if link.status < 0:
            if link.status == pySerialTransfer.CRC_ERROR:
                logger.error("ERROR: CRC_ERROR")
            elif link.status == pySerialTransfer.PAYLOAD_ERROR:
                logger.error("ERROR: PAYLOAD_ERROR")
            elif link.status == pySerialTransfer.STOP_BYTE_ERROR:
                logger.error("ERROR: STOP_BYTE_ERROR")
            else:
                logger.error("ERROR: link status {}".format(link.status))

    ###################################################################
    # Parse response
    ###################################################################
    rec = link.rx_obj(
        obj_type=(list), byte_format="<", list_format="i", obj_byte_size=send_size
    )
    if rec is None:
        return False
    logger.debug("received {} of length {} bytes.", rec, send_size)
    return True
