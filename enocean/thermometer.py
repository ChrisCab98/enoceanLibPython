from mqtt.client import MqttClient
from mqtt.interfaceconnector import IMqttConnector
import time
import json


class Thermometer(IMqttConnector):
    def __init__(self, ID, topicToPublish):
        super().__init__()
        # switch properties
        self.__uniqueID = ID

        # packet payload
        self.__packet = ""
        self.__RSSI = 0
        self.__temperature = 0

        # Topics
        # Set
        self.__setTemperatureTopic = topicToPublish

        # Bridge enOcean
        self.__topicEnocean = "enocean/device/id/{}".format(self.__uniqueID)

        print("[Thermometer] with uniqueID {} opened".format(self.__uniqueID))

        # Instanciate MQTT Client
        self.__mqtt = MqttClient(self, "127.0.0.1", [
                                 self.__topicEnocean, ], "TemperatureSensor-"+self.__uniqueID)

    def Receive(self, server, topic: str, payload: bytes):

        print("[MQTT] " + topic)

        self.__packet = payload.decode("utf-8")

        msg = json.loads(self.__packet)
        print("[MQTT] " + str(msg['packet']))

        self.__temperature = int(str(msg['packet']["data"]["DB1"]), 16)*40/250

        self.Send(self.__setTemperatureTopic, str(self.__temperature))

    def Send(self, topic, msg):
        self.__mqtt.sendMessage(topic, msg)

    def Connected(self, server):
        pass

    def Acknowledge(self, server, messageId: int):
        pass

    def Stop(self):
        print("[Thermometer] with uniqueID {} closed".format(self.__uniqueID))
