import json
import time
from datetime import datetime, timedelta

from mqtt.client import MqttClient
from mqtt.interfaceconnector import IMqttConnector


class Switch(IMqttConnector):
    def __init__(self, enOceanID, deviceProperties: dict):
        super().__init__()

        # switch properties
        self.__enOceanID = enOceanID
        self.__deviceProperties = deviceProperties
        self.__topicDevices = {}
        self.__dimmerValue = 0
        self.__channel = ""

        self.__enOceanTopic = "enocean/device/id/{}".format(self.__enOceanID)

        self.__timestamp1 = None
        self.__timestamp2 = None
        self.__deltaTime = None
        self.__formatDate = "%d/%m/%y %H:%M:%S.%f"

        self.createDictOfTopics(self.__deviceProperties)

        print("[Switch] with uniqueID {} opened".format(self.__enOceanID))

        # Instanciate MQTT Client
        self.__mqtt = MqttClient(self, "127.0.0.1", [
                                 self.__enOceanTopic, self.__topicDevices], "Switch-"+self.__enOceanID)

    def createDictOfTopics(self, deviceProperties):
        for x in self.__deviceProperties["device"]:
            powerTopics = "cmnd/{}/power{}".format(
                self.__deviceProperties["device"][x]["MQTTName"], self.__deviceProperties["device"][x]["channel"])

            if self.__deviceProperties["device"][x]["dimmable"] == True:
                dimmerTopics = "cmnd/{}/dimmer".format(
                    self.__deviceProperties["device"][x]["MQTTName"])

                self.__topicDevices[str(x)] = {
                    "power": powerTopics, "dimmer": dimmerTopics}

            else:
                self.__topicDevices[str(x)] = {
                    "power": powerTopics}

    def sendBrightness(self, topics):
        print(topics)

        if self.__deltaTime < timedelta(milliseconds=250):
            print("[INFO] less than 250ms press")
            self.Send(topics, "25")

        if timedelta(milliseconds=250) < self.__deltaTime < timedelta(milliseconds=500):
            print("[INFO] press between 250 & 500ms")
            self.Send(topics, "50")

        if timedelta(milliseconds=500) < self.__deltaTime < timedelta(milliseconds=750):
            print("[INFO] press between 500 & 750ms")
            self.Send(topics, "75")

        if self.__deltaTime > timedelta(milliseconds=750):
            print("[INFO] press longer than 750ms")
            self.Send(topics, "100")

        print("[INFO] DeltaTime : " + str(self.__deltaTime))

    def Receive(self, server, topic: str, payload: bytes):
        self.__packet = payload.decode("utf-8")

        msg = json.loads(self.__packet)
        # print("[MQTT] " + str(msg['packet']))

        self.__RSSI = int(msg['packet']['optionalData']['dBm'], 16)
        self.__state = msg['packet']['data']['status']

        if self.__state == "30":
            self.__channel = msg['packet']['data']['data']
            print("[INFO] Pressed on channel {}".format(self.__channel))

            self.__timestamp1 = datetime.strptime(
                datetime.now().strftime("%d/%m/%y %H:%M:%S.%f"), self.__formatDate)

        else:
            # print("[INFO] Released on channel {}".format(self.__channel))
            self.__timestamp2 = datetime.strptime(
                datetime.now().strftime("%d/%m/%y %H:%M:%S.%f"), self.__formatDate)

            self.__deltaTime = self.__timestamp2 - self.__timestamp1

            if self.__channel == "10":
                if self.__deviceProperties["device"]["0"]["dimmable"] == True:
                    self.sendBrightness(self.__topicDevices["0"]["dimmer"])
                else:
                    self.Send(self.__topicDevices["0"]["power"], "TOGGLE")

            if self.__channel == "30":
                if self.__deviceProperties["device"]["1"]["dimmable"] == True:
                    self.sendBrightness(self.__topicDevices["1"]["dimmer"])
                else:
                    self.Send(self.__topicDevices["1"]["power"], "TOGGLE")

            if self.__channel == "50":
                if self.__deviceProperties["device"]["2"]["dimmable"] == True:
                    self.sendBrightness(self.__topicDevices["2"]["dimmer"])
                else:
                    self.Send(self.__topicDevices["2"]["power"], "TOGGLE")

            if self.__channel == "70":
                if self.__deviceProperties["device"]["3"]["dimmable"] == True:
                    self.sendBrightness(self.__topicDevices["3"]["dimmer"])
                else:
                    self.Send(self.__topicDevices["3"]["power"], "TOGGLE")

    def Send(self, topic, msg):
        self.__mqtt.sendMessage(topic, msg)

    def Connected(self, server):
        pass

    def Acknowledge(self, server, messageId: int):
        pass

    def Stop(self):
        print("[Switch] with uniqueID {} closed".format(self.__enOceanID))
