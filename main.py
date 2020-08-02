from console.uart import Uart
from enocean.switch import Switch
from enocean.thermometer import Thermometer
from enocean.humiditySensor import HumiditySensor
import time

myUart = Uart()
mySwitch1 = Switch("0032b591", "SmartSurgeDesk", channel="1")
mySwitch2 = Switch("0032b5c0", "LightChrisRoom", dimmable=True)
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
MyThermometer.Stop()
MyHumiditySensor.Stop()
