from threading import Thread
from serial import Serial
from datetime import datetime, timedelta
import time
from mqtt.interfaceconnector import IMqttConnector
from mqtt.client import MqttClient


class Uart():
    class Receiver(Thread, IMqttConnector):
        def __init__(self, handle):
            super().__init__()
            self.__running = True
            self.__handle: Serial = handle

            self.__mqtt = MqttClient(self, "localhost", "")
            self.__topic = ""

            self.__datas = []
            self.__syncByte: str = "55"
            self.__byte: str = []
            self.__uniqueID = ""
            self.run()

        def Receive(self, server, topic: str, payload: bytes):
            pass

        def Connected(self, server):
            pass

        def Acknowledge(self, server, messageId: int):
            pass

        def Send(self, topics, msg):
            self.__mqtt.sendMessage(self.__topic, msg)

        def run(self) -> None:
            while self.__running:
                self.__byte = (self.__handle.read(1).hex())
                # Check for SyncByte
                if self.__byte == self.__syncByte:
                    print("[UART] Start receiving enOcean packet")

                    # Start saving packet with sync byte
                    self.__datas.append(self.__byte)

                    # Add the rest of the packet
                    for x in range(0, 20):
                        self.__datas.append(self.__handle.read(1).hex())

                    # Extract uniqueID for packet
                    self.__uniqueID = self.__datas[8]
                    self.__uniqueID += self.__datas[9]
                    self.__uniqueID += self.__datas[10]
                    self.__uniqueID += self.__datas[11]

                    print("[UART] UniqueID : " + self.__uniqueID)

                    self.__topic = "enocean/device/id/{}".format(
                        self.__uniqueID)

                    # Send packet to topics with uniqueID
                    self.Send(self.__topic, str(self.__datas))

                self.__datas.clear()

        def Stop(self):
            self.__running = False
            self.__handle.cancel_read()
            print("[UART] Serial line closed")

    def __init__(self):
        self.__SerialPortName = "/dev/ttyAMA0"
        self.__SerialPortSpeed = "57600"
        self.__handle = Serial(self.__SerialPortName,
                               self.__SerialPortSpeed, timeout=2.0)
        print(("[UART] Serial line {} @ {} bauds opened".format(
            self.__SerialPortName, self.__SerialPortSpeed)))
        self.__thread: Uart.Receiver = self.Receiver(self.__handle)

    def Stop(self):
        self.__thread.Stop()
