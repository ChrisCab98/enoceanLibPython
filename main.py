from console.uart import Uart
# from enocean.switch import Switch
from enocean.newSwitch import Switch
from enocean.thermometer import Thermometer
from enocean.humiditySensor import HumiditySensor
import time

deviceProperties1 = {
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
                "MQTTName": "SmartSurgeDesk",
                "channel": 1,
                "dimmable": True
            }
        }

}

deviceProperties2 = {
    "device":
        {
            "0":
            {
                "MQTTName": "SmartSurgeDesk",
                "channel": 1,
                "dimmable": False
            },
            "1":
            {
                "MQTTName": "SmartSurgeDesk",
                "channel": 2,
                "dimmable": False
            },
            "2":
            {
                "MQTTName": "SmartSurgeDesk",
                "channel": 3,
                "dimmable": False
            },
            "3":
            {
                "MQTTName": "SmartSurgeDesk",
                "channel": 4,
                "dimmable": False
            }
        }

}

deviceProperties3 = {
    "device":
        {
            "0":
            {
                "MQTTName": "LightChrisRoom",
                "channel": 1,
                "dimmable": True
            },
            "1":
            {
                "MQTTName": "LightChrisRoom",
                "channel": 1,
                "dimmable": False
            }
        }

}

myUart = Uart()
mySwitch1 = Switch("0032b591", deviceProperties1)
mySwitch2 = Switch("0032cd29", deviceProperties2)
mySwitch3 = Switch("0032b5c0", deviceProperties3)

MyThermometer = Thermometer("05103dbe", "getCurrentTemperature/TRIO2SYS")
MyHumiditySensor = HumiditySensor(
    "05103dbe", "getCurrentRelativeHumidity/TRIO2SYS")

# Run...
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break

myUart.Stop()
mySwitch1.Stop()
mySwitch2.Stop()
mySwitch3.Stop()
MyThermometer.Stop()
MyHumiditySensor.Stop()
