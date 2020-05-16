import time
import signal
#from rd import recordIt
from tools import *


# signal trap to handle keyboard interrupt
signal.signal(signal.SIGINT, signal_handler)
print("[INFO] Press `ctrl + c` to exit, or 'q' to quit if you have" \
	" the display option on...")
s = state()
i = 0
while True:    
    print("Detected")
    conf = "My conf"
    #recordIt(i, conf)
    print(str(s.fibo(i)))
    i = i + 1
    time.sleep(1.0)

