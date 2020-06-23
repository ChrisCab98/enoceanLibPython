from threading import Thread
from serial import Serial
from datetime import datetime, timedelta
import time
import json
from mqtt.interfaceconnector import IMqttConnector
from mqtt.client import MqttClient


class Uart:
    class Receiver(Thread, IMqttConnector):
        def __init__(self, handle):
            super().__init__()
            self.__running = True
            self.__handle: Serial = handle

            # MQTT
            self.__mqtt = MqttClient(self, "raspberrypi.local", "")
            self.__topic = ""

            # enOcean packet
            self.__packet = {}
            self.__rawPacket = []
            self.__syncByte = "55"
            self.__byte = ""
            self.__uniqueID = "00:00:00:00"
            self.start()

        def Receive(self, server, topic: str, payload: bytes):
            pass

        def Connected(self, server):
            pass

        def Acknowledge(self, server, messageId: int):
            pass

        def Send(self, topics, msg):
            jsonMsg = {
                'packet':
                {
                    'header':
                    {
                        'syncByte': msg[0],
                        'dataLength': msg[1]+msg[2],
                        'optionalDataLength': msg[3],
                        'packetType': msg[4]

                    },
                    'data':
                    {
                        'RORG': msg[6],
                        'data': msg[7],
                        'senderID': msg[8]+msg[9]+msg[10]+msg[11],
                        'status': msg[12]
                    },
                    'optionalData':
                    {
                        'subTelNum': msg[13],
                        'destinationID': msg[14]+msg[15]+msg[16]+msg[17],
                        'dBm': msg[18],
                        'securityLevel': msg[19]
                    }
                }
            }
            # print(jsonMsg)
            jsonMsg = json.dumps(jsonMsg)
            self.__mqtt.sendMessage(self.__topic, jsonMsg)

        def run(self) -> None:
            while self.__running:
                self.__byte = (self.__handle.read(1).hex())
                # print(self.__byte)
                # Check for SyncByte
                if self.__byte == self.__syncByte:
                    print("[UART] Start receiving enOcean packet")

                    # Start saving packet with sync byte
                    self.__rawPacket.append(self.__byte)

                    # Add the rest of the packet
                    for x in range(0, 20):
                        self.__rawPacket.append(self.__handle.read(1).hex())

                    # Extract uniqueID for packet
                    self.__uniqueID = self.__rawPacket[8]
                    self.__uniqueID += self.__rawPacket[9]
                    self.__uniqueID += self.__rawPacket[10]
                    self.__uniqueID += self.__rawPacket[11]

                    print("[UART] packet from : " +
                          self.__uniqueID)

                    self.__topic = "enocean/device/id/{}".format(
                        self.__uniqueID)

                    # Send packet to topics with uniqueID
                    self.Send(self.__topic, self.__rawPacket)

                self.__rawPacket.clear()

        def Stop(self):
            print("[UART] Serial line closed")
            self.__running = False
            self.__handle.cancel_read()

    def __init__(self):
        self.__SerialPortName = "/dev/ttyAMA0"
        self.__SerialPortSpeed = "57600"
        self.__handle = Serial(self.__SerialPortName,
                               self.__SerialPortSpeed, timeout=2.0)
        print(("[UART] Serial line {} @ {} bauds opened".format(
            self.__SerialPortName, self.__SerialPortSpeed)))
        self.__thread: Uart.Receiver = self.Receiver(self.__handle)

    def __del__(self):
        self.Stop()
        self.__handle.close()

    def Stop(self):
        self.__thread.Stop()
