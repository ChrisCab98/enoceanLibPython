from threading import Thread
from serial import Serial
from datetime import datetime, timedelta
import time


class Uart():
    class Receiver(Thread):
        def __init__(self, handle):
            super().__init__()
            self.__running = True
            self.__handle: Serial = handle
            self.__datas = []
            self.__syncByte: str = "55"
            self.__byte: str = []
            self.__timePushed = None
            self.__timeReleased = None
            self.__currentTime = None
            self.__deltaTime = None
            self.__isPush = "30"
            self.__RSSI = 0
            self.__formatDate = "%d/%m/%y %H:%M:%S.%f"
            self.run()

        def run(self):
            while self.__running:
                self.__byte = (self.__handle.read(1).hex())
                # Check for SyncByte
                if self.__byte == self.__syncByte:
                    print("Start receiving enOcean packet")

                    # Get current time
                    self.__currentTime = datetime.strptime(
                        datetime.now().strftime("%d/%m/%y %H:%M:%S.%f"), self.__formatDate)

                    # Start saving packet with sync byte
                    self.__datas.append(self.__byte)

                    # Add the rest of the packet
                    for x in range(0, 20):
                        self.__datas.append(self.__handle.read(1).hex())

                    # print the datas
                    print(self.__datas)

                    # check if swith have been pressed or released
                    if self.__datas[12] == self.__isPush:
                        self.__timePushed = self.__currentTime
                        print("PRESS")

                    else:
                        self.__timeReleased = self.__currentTime
                        print("RELEASE")

                    # Calculate the dela time between presse and release
                    try:
                        self.__deltaTime = self.__timeReleased - self.__timePushed
                        print(self.__deltaTime)
                        self.__timeReleased = 0
                        self.__timePushed = 0
                    except:
                        print("Switch hasn't been relased yet")

                    self.__RSSI = int(self.__datas[18], 16)
                    print("RSSI : -" + str(self.__RSSI) + " dBm")

                self.__datas.clear()

        def Stop(self):
            self.__running = False
            self.__handle.cancel_read()
            print("[UART] Serial line closed")

    def __init__(self):
        super().__init__()
        self.__SerialPortName = "/dev/ttyAMA0"
        self.__SerialPortSpeed = "57600"
        self.__handle = Serial(self.__SerialPortName,
                               self.__SerialPortSpeed, timeout=2.0)
        print(("[UART] Serial line {} @ {} bauds opened".format(
            self.__SerialPortName, self.__SerialPortSpeed)))
        self.__thread = self.Receiver(self.__handle)

    def Stop(self):
        self.__thread.Stop()
