import os
from typing import List
from datetime import datetime, timedelta

deviceProperties = {
    "device":
        {
            "0":
            {
                "MQTTName": "sonoffFan",
                "channel": 1,
                "dimmable": False
            },
            "1":
            {
                "MQTTName": "columnLED",
                "channel": 4,
                "dimmable": True
            },
            "2":
            {
                "MQTTName": "powerOutletBed",
                "channel": 2,
                "dimmable": False
            }
        }

}


class TestSwitch:

    def __init__(self, enOceanID, deviceProperties):
        self.__enOceanID = enOceanID
        self.__deviceProperties = deviceProperties
        self.__topicDevices = {}
        self.__dimmerValue = 0

        self.__timestamp1 = None
        self.__timestamp2 = None
        self.__deltaTime = None
        self.__formatDate = "%d/%m/%y %H:%M:%S.%f"

        self.createDictOfTopics(self.__deviceProperties)

        print(self.__topicDevices)

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

    def Send(self, topic, msg):
        print("Sending")


os.system('clear')
mySwitch = TestSwitch("b598f378", deviceProperties)
