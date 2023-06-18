import os
import torch
import random

import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from collections import deque

from utilities import get_git_root, normalize
from model import MIMOLSTM
from PID import PID

LOOKBACK = 100
LOOKFORWARD = 50
GIT_ROOT = get_git_root()
LOG_FOLDER = os.path.join(GIT_ROOT,"XX_logs","logs")
LOGS = os.listdir(LOG_FOLDER)
STATEDICT_TO_LOAD = "mimo_lstm_statedict_normalized.pt"
#STATEDICT_TO_LOAD = "mimo_lstm_statedict.pt"


print("loading logs")
full_logs = []

for log in tqdm(LOGS):
    full_logs.append(torch.load(os.path.join(LOG_FOLDER,log,"logfile.pt")))
topick = ["Thr","Ail","Elev","Rudd","Roll","Pitch",
          "Yaw","Spd","GyrX","GyrY","GyrZ","AccX","AccY","AccZ"]

full_logs = torch.Tensor(normalize(pd.concat(full_logs)[topick]).values)
#full_logs = torch.Tensor(pd.concat(full_logs)[topick].values)

model = MIMOLSTM(input_size=len(topick),lookback=LOOKBACK)
model.load_state_dict(torch.load(
        os.path.join(GIT_ROOT,"XX_logs","statedicts",STATEDICT_TO_LOAD)
))
model.eval()

#skip boring part randomly
SKIP = random.choice(range(LOOKBACK,len(full_logs)))
plot_bars = False

#heat control
CONTROL_CONSTANTS = [.1,1,0]
FUTURE_CONTROLLER_CONSTANTS = [0.1,0.1,0]
FUTURE_NOW_CONTROLLER_CONSTANTS = [0,0,0]
pres_pid = PID(*CONTROL_CONSTANTS)
fut_pid = PID(*FUTURE_CONTROLLER_CONSTANTS)
fut_now_pid = PID(*FUTURE_NOW_CONTROLLER_CONSTANTS)
fut_heat = .20
pres_heat = .20
set_temp = .20
pres_heat_queue = deque([],LOOKBACK)
fut_heat_queue = deque([],LOOKBACK)
fut_control_inputs_q = deque([set_temp]*2,2)

for it, _ in enumerate(full_logs, LOOKBACK+SKIP):
    logs_to_look_at = full_logs[-LOOKBACK+it:it,:].unsqueeze(0)
    for i in range(LOOKFORWARD-1):
        data_pred = model.forward(logs_to_look_at)
        logs_to_look_at = torch.cat(
            [logs_to_look_at[:,1:,:],
             data_pred.unsqueeze(0).unsqueeze(1)],
             dim=1)
    
    
    gt = full_logs[it:it+LOOKFORWARD,0].detach().numpy()
    pred = logs_to_look_at[0,-LOOKFORWARD-2:,0].detach().numpy()
    
    # control on the most recent point
    # future control: seems to be wrong approach, tries to get rid of heat
    # before it appears. but get rid of heat WHEN it appears
    # -> calculate heat and then the neccessary control input
    # e.g. how much throttle is expected -> how much heat -> how much cooling
    # at certain time step.
    pres_cont_inp = pres_pid.step(set_temp,pres_heat)
    exp_heat = fut_heat+(sum(pred[:len(fut_control_inputs_q)])/len(fut_control_inputs_q))*0.3
    fut_cont_inp = fut_pid.step(set_temp,(exp_heat*0.5))
    fut_control_inputs_q.append(fut_cont_inp)

    pres_heat += (logs_to_look_at[0,0,0].detach().numpy()*0.3) - pres_cont_inp
    fut_heat -= (fut_control_inputs_q[0]*0.5+
        fut_now_pid.step(set_temp,fut_heat)*0.5)
    if abs(fut_cont_inp) > 1000:
        print("future control input over 1000")
        exit()
    pres_heat_queue.append(pres_heat)
    fut_heat_queue.append(fut_heat)

    
    plt.grid(True)
    plt.plot(range(-len(pres_heat_queue),0),pres_heat_queue,"green")
    plt.plot(range(-len(fut_heat_queue),0),fut_heat_queue,"violet")
    plt.savefig("pid_only.png")
    plt.plot(range(-100,0),full_logs[-LOOKBACK+it:it,0])
    plt.plot(pred,"red")
    plt.plot(gt,"blue")
    plt.title("blue = ground truth; red = prediction; green pid without pred")
    plt.savefig("pidtest.png")
    plt.clf()
    print(it, end = "\r")
plt.show()