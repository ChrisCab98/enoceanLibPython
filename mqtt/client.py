import paho.mqtt.client as mqtt
from threading import Thread
from typing import List
from mqtt.interfaceconnector import IMqttConnector


class MqttClient(Thread):
    def __init__(self, reader: IMqttConnector, host, topics: List[str], clientID):
        super().__init__()
        self.__clientid = clientID
        self.__host = host
        self.__topics: List[str] = topics

        # Initiate MQTT Client
        self.__client = mqtt.Client(
            client_id=self.__clientid, clean_session=True)

        # Register publish callback function
        self.__client.on_publish = self.__OnPublish
        self.__client.on_connect = self.__OnConnect
        self.__client.on_message = self.__OnMessage
        self.__client.user_data_set(reader)

        # Run the server
        self.__client.connect(host)
        self.start()

        if len(self.__topics) > 0:
            print("[MQTT] {} listening from {} on topics:".format(
                self.__clientid, self.__host))
        else:
            print("[MQTT] {} ready to send messages to {}".format(
                self.__clientid, self.__host))

    def __del__(self):
        self.Halt()

    def run(self):
        self.__client.loop_forever()

    def Halt(self):
        print("[MQTT] {} Disconnect from MQTT server {}".format(
            self.__clientid, self.__host))
        self.__client.disconnect()

    def sendMessage(self, topic: str, message: bytes):
        self.__client.publish(topic, message, qos=2)

    def __OnMessage(self, client, userdata, msg):
        userdata.Receive(self, msg.topic, msg.payload)

    def __OnConnect(self, mqttc, userdata, flags, rc):
        # Subscribe to a Topic
        if rc == 0:
            for topic in self.__topics:
                mqttc.subscribe(topic, 2)
                print("[MQTT] {} Subscribed to: {}".format(
                    self.__clientid, topic))
            print("[MQTT] {} Connected.".format(self.__clientid))
        else:
            print("[MQTT] {} Bad connection. Returned code = {}".format(
                self.__clientid, rc))
            exit()
        userdata.Connected(self)

    def __OnPublish(self, _, userdata, mid: int):
        # LOG.debug("Message {} Published...".format(mid))
        userdata.Acknowledge(self, mid)
