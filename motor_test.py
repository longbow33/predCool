import matplotlib.pyplot as plt
import time
from simple_pid import PID

from electric_motor import Motor
from loader import Loader


attributes_to_pick = ["Thr","Ail","Elev","Rudd","Roll","Pitch",
          "Yaw","Spd","GyrX","GyrY","GyrZ","AccX","AccY","AccZ"]
loader = Loader(attributes_to_pick)
logs = loader.load()


controller_motor = PID(1,1,1,setpoint=20,output_limits=(0.1,1000))


motor = Motor(20,100)
heats = [20]
cont_inp_list = []
for i in range(logs.shape[0]):
    cont_inp = controller_motor(motor.temperature)
    heats.append(motor.step(logs[i,0],cont_inp,0))
    cont_inp_list.append(cont_inp)
    plt.grid(True)
    plt.plot(heats,"red")
    plt.plot(logs[:i,0],"blue")
    plt.savefig("motor_sim.png")
    plt.clf()
    plt.grid(True)
    plt.plot(cont_inp_list)
    plt.savefig("cont_inputs.png")
    plt.clf()
    time.sleep(.1)
