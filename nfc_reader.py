import logging
from threading import Thread

import RPi.GPIO as GPIO
import SimpleMFRC522

import time

from kalliope.core.SynapseLauncher import SynapseLauncher

from kalliope import Utils
from kalliope.core import SignalModule

logging.basicConfig()
logger = logging.getLogger("kalliope")


class RFIDReader(SignalModule, Thread):

    def __init__(self, **kwargs):
        super(RFIDReader, self).__init__(**kwargs)
        Thread.__init__(self, name=RFIDReader)
        Utils.print_info('[NFC_Reader] Starting manager ...')
        self.synapse_list = list(super(RFIDReader, self).get_list_synapse())
        if self.synapse_list is None:
            self.synapse_list = list()

    def run(self):
        logger.debug("[NFC_Reader] Starting thread ...")

        self.reader = SimpleMFRC522.SimpleMFRC522()

        try:
            while True:
                user_id = reader.read()
                for synapse in self.synapse_list:
                    SynapseLauncher.start_synapse_by_list_name([synapse], args=[user_id])
                time.sleep(0.1)
        except KeyboardInterrupt:
        finally:
            GPIO.cleanup()
