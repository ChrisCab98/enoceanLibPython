from console.uart import Uart
from enocean.switch import Switch
import time

print("Start")
myUart = Uart()
print("UART done")
mySwitch1 = Switch("0032b591", "light")

# Run...
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break

myUart.Stop()
mySwitch1.Stop()
