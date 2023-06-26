import matplotlib.pyplot as plt
import time
from simple_pid import PID
from collections import deque

from electric_motor import Motor
from loader import Loader


attributes_to_pick = ["Thr","Ail","Elev","Rudd","Roll","Pitch",
          "Yaw","Spd","GyrX","GyrY","GyrZ","AccX","AccY","AccZ"]
loader = Loader(attributes_to_pick)
logs = loader.load()


controller_motor = PID(.01,100,0,setpoint=20,output_limits=(.0001,1000000))


motor = Motor(20,100)
heats = deque([],maxlen=100)
cont_inp_list = deque([],maxlen=100)
for i in range(logs.shape[0]):
    cont_inp = controller_motor(motor.temperature)
    heats.append(int(motor.step(logs[i,0],cont_inp,1)))
    cont_inp_list.append(cont_inp)
    plt.grid(True)
    plt.title("Heat: Red, Thrust: Blue")
    plt.plot(heats,"red")
    plt.plot(logs[i-100:i,0],"blue")
    plt.savefig("motor_sim.png")
    plt.clf()
    plt.grid(True)
    plt.plot(cont_inp_list)
    plt.savefig("cont_inputs.png")
    plt.clf()
    time.sleep(.1)
