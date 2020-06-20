from console.uart import Uart
import time

myUart = Uart()

# Run...
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break

myUart.Stop()
