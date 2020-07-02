from mqtt.client import MqttClient
from mqtt.interfaceconnector import IMqttConnector
import time
import json
from datetime import datetime, timedelta


class Switch(IMqttConnector):
    def __init__(self, ID, device, channel="", dimmable=False):
        super().__init__()
        # switch properties
        self.__uniqueID = ID
        self.__device = device
        self.__dimmable = dimmable
        self.__channel = channel
        self.__deviceStatus = ""
        self.__dimmerValue: int

        # packet payload
        self.__state = ""
        self.__packet = ""
        self.__RSSI = 0
        self.__timestamp1 = None
        self.__timestamp2 = None
        self.__deltaTime = None

        self.__formatDate = "%d/%m/%y %H:%M:%S.%f"

        # Topics
        # Get
        self.__topicResult = "stat/{}/RESULT".format(self.__device)
        # Set
        self.__topicsCmndDeviceDimmer = "cmnd/{}/dimmer".format(self.__device)
        self.__topicsCmndDevice = "cmnd/{}/power{}".format(
            self.__device, self.__channel)

        # Bridge enOcean
        self.__topicEnocean = "enocean/device/id/{}".format(self.__uniqueID)

        print("[Switch] with uniqueID {} opened".format(self.__uniqueID))

        # Instanciate MQTT Client
        self.__mqtt = MqttClient(self, "127.0.0.1", [
                                 self.__topicResult, self.__topicEnocean])

        self.getStatus()

    def Receive(self, server, topic: str, payload: bytes):

        print("[MQTT] " + topic)

        # RESULT
        if topic == self.__topicResult:
            try:
                dimmerValues = payload.decode("utf-8")
                msg = json.loads(dimmerValues)
                self.__dimmerValue = int(msg['Dimmer'])
                print("[MQTT] Dimmer : " + str(self.__dimmerValue))
            except:
                pass

            try:
                deviceStatus = payload.decode("utf-8")
                msg = json.loads(deviceStatus)
                # powerChannel = "POWER{}".format(self.__channel)
                self.__deviceStatus = (msg['POWER{}'.format(self.__channel)])
                print("[MQTT] Status : " + str(self.__deviceStatus))
            except:
                pass

        if topic == self.__topicEnocean:
            self.__packet = payload.decode("utf-8")

            msg = json.loads(self.__packet)
            print("[MQTT] " + str(msg['packet']))

            self.__RSSI = int(msg['packet']['optionalData']['dBm'], 16)
            self.__state = msg['packet']['data']['status']

            if self.__state == "30":
                self.__timestamp1 = datetime.strptime(
                    datetime.now().strftime("%d/%m/%y %H:%M:%S.%f"), self.__formatDate)

            else:
                self.__timestamp2 = datetime.strptime(
                    datetime.now().strftime("%d/%m/%y %H:%M:%S.%f"), self.__formatDate)

                print("[INFO] Button pressed then released !")

                self.__deltaTime = self.__timestamp2 - self.__timestamp1

                if self.__dimmable == True:
                    if self.__dimmerValue == 0:
                        if self.__deltaTime < timedelta(milliseconds=250):
                            print("[INFO] less than 250ms press")
                            self.Send(self.__topicsCmndDeviceDimmer, "25")

                        if timedelta(milliseconds=250) < self.__deltaTime < timedelta(milliseconds=500):
                            print("[INFO] press between 250 & 500ms")
                            self.Send(self.__topicsCmndDeviceDimmer, "50")

                        if timedelta(milliseconds=500) < self.__deltaTime < timedelta(milliseconds=750):
                            print("[INFO] press between 500 & 750ms")
                            self.Send(self.__topicsCmndDeviceDimmer, "75")

                        if self.__deltaTime > timedelta(milliseconds=750):
                            print("[INFO] press longer than 750ms")
                            self.Send(self.__topicsCmndDeviceDimmer, "100")

                        print("[INFO] DeltaTime : " + str(self.__deltaTime))
                    else:
                        self.Send(self.__topicsCmndDevice, "OFF")
                        self.Send(self.__topicsCmndDeviceDimmer, "0")

                else:
                    self.invertStatus()

    def Send(self, topic, msg):
        self.__mqtt.sendMessage(topic, msg)

    def Connected(self, server):
        pass

    def Acknowledge(self, server, messageId: int):
        pass

    def Stop(self):
        print("[Switch] with uniqueID {} closed".format(self.__uniqueID))

    def getStatus(self):
        self.Send(self.__topicsCmndDevice, "")
        self.Send(self.__topicsCmndDeviceDimmer, "")

    def invertStatus(self):
        if self.__deviceStatus == "ON":
            self.Send(self.__topicsCmndDevice, "OFF")

        if self.__deviceStatus == "OFF":
            self.Send(self.__topicsCmndDevice, "ON")
