from collections import deque
import matplotlib.pyplot as plt
import time
from simple_pid import PID
from torch import nn

from electric_motor import Motor
from loader import Loader

# constants
VOLUME_HEAT_RESERVOIR = .010
SKIP = 2500

attributes_to_pick = ["Thr","Ail","Elev","Rudd","Roll","Pitch",
          "Yaw","Spd","GyrX","GyrY","GyrZ","AccX","AccY","AccZ"]
loader = Loader(attributes_to_pick)
logs = loader.load()


controller_motor = PID(-.00001,-.00001,0,setpoint=180,output_limits=(0,1000))

motor = Motor(init_temperature = 180,volume_reservoir = VOLUME_HEAT_RESERVOIR)
heats = deque([],maxlen=100)
cont_inp_list = deque([],maxlen=100)
for i in range(SKIP,logs.shape[0]):
    cont_inp = controller_motor(motor.temperature)
    heats.append(int(motor.step(logs[i,0],cont_inp,20)))
    cont_inp_list.append(cont_inp)
    loss = sum([abs(x-180) for x in heats])/len(heats)+sum([abs(x) for x in cont_inp_list])/len(cont_inp_list)
    print(
        f"HeatBal: {motor.current_heat_balance:2.2f}kW  \tTemp: {motor.temperature:.2f}\tThrust:{int(logs[i,0])}\tContInput {cont_inp:.3e}\tloss: {loss:.3f}")
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
