from threading import Thread
from datetime import datetime, timedelta
import time
from mqtt.interfaceconnector import IMqttConnector
from mqtt.client import MqttClient


class Switch(Thread, IMqttConnector):
    def __init__(self, ID, device):
        super().__init__()
        self.__uniqueID = ID
        self.__device = device
        self.__state = ""

        self.__topics = "stat/{}/POWER".format(self.__device)
        self.__running = True

        print("[Switch] with uniqueID {} opened".format(self.__uniqueID))

        self.__mqtt = MqttClient(self, "localhost", self.__topics)

        self.run()

    def Receive(self, server, topic: str, payload: bytes):
        pass

    def Connected(self, server):
        pass

    def Acknowledge(self, server, messageId: int):
        pass

    def run(self):
        while self.__running:
            # print("switch thread")
            pass

    def Stop(self):
        self.__running = False
        print("[Switch] with uniqueID {} closed".format(self.__uniqueID))
