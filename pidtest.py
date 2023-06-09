import math
from collections import deque
import matplotlib.pyplot as plt

from PID import PID

MAXLEN = 1000

pid = PID(1,.5,.1)
heat = 0
heat_deque = deque([],MAXLEN)
x_deque = deque([],MAXLEN)

x = 0
for i in range(1000):
    if i%50 == 0:
        if i%100 == 0:
            x+=1
        else:
            x-= 1
    heat += x-pid.step(0,heat)
    heat_deque.append(heat)
    x_deque.append(x)
    plt.plot(x_deque,"red")
    plt.plot(heat_deque,"blue")
    plt.grid(True)
    plt.pause(.1)
    plt.clf()
plt.show()
