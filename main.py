from console.uart import Uart
from enocean.switch import Switch
import time

myUart = Uart()
mySwitch1 = Switch("0032b591", "light")
mySwitch1 = Switch("0032b5c0", "light2")

# Run...
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break

myUart.Stop()
mySwitch1.Stop()
