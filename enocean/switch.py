from mqtt.client import MqttClient
from mqtt.interfaceconnector import IMqttConnector
import time
import json
from datetime import datetime, timedelta


class Switch(IMqttConnector):
    def __init__(self, ID, device, dimmable=False):
        super().__init__()
        self.__uniqueID = ID
        self.__device = device

        self.__deviceStatus = ""

        # packet payload
        self.__state = ""
        self.__packet = ""
        self.__RSSI = 0
        self.__timestamp1 = None
        self.__timestamp2 = None

        self.__formatDate = "%d/%m/%y %H:%M:%S.%f"

        self.__topicsDevice = "stat/{}/POWER".format(self.__device)
        self.__topicsCmndDevice = "cmnd/{}/power".format(self.__device)
        # self.__running = True
        print("[Switch] with uniqueID {} opened".format(self.__uniqueID))

        # Instanciate MQTT Client
        self.__mqtt = MqttClient(self, "raspberrypi.local", [
                                 self.__topicsDevice, "enocean/device/id/{}".format(self.__uniqueID)])

    def Receive(self, server, topic: str, payload: bytes):

        print(topic)

        if topic == self.__topicsDevice:
            self.__deviceStatus = payload.decode("utf-8")
            print(self.__deviceStatus)

        else:
            self.__packet = payload.decode("utf-8")

            msg = json.loads(self.__packet)
            print(msg['packet'])

            self.__RSSI = int(msg['packet']['optionalData']['dBm'], 16)
            self.__state = msg['packet']['data']['status']

            if self.__state == "30":
                self.__timestamp1 = datetime.strptime(
                    datetime.now().strftime("%d/%m/%y %H:%M:%S.%f"), self.__formatDate)

            else:
                self.__timestamp2 = datetime.strptime(
                    datetime.now().strftime("%d/%m/%y %H:%M:%S.%f"), self.__formatDate)
                print("Button press then released !")

                if self.__deviceStatus == "ON":
                    self.Send("off")
                if self.__deviceStatus == "OFF":
                    self.Send("on")
                else:
                    self.Send("")

    def Send(self, msg):
        self.__mqtt.sendMessage(self.__topicsCmndDevice, msg)

    def Connected(self, server):
        pass

    def Acknowledge(self, server, messageId: int):
        pass

    def Stop(self):
        # self.__running = False
        print("[Switch] with uniqueID {} closed".format(self.__uniqueID))

    def getStatus(self):
        self.Send("")
