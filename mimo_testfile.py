import os
import torch

import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from collections import deque

from utilities import get_git_root, normalize
from model import MIMOLSTM
from PID import PID

LOOKBACK = 100
LOOKFORWARD = 100
GIT_ROOT = get_git_root()
LOG_FOLDER = os.path.join(GIT_ROOT,"XX_logs","logs")
LOGS = os.listdir(LOG_FOLDER)
#STATEDICT_TO_LOAD = "mimo_lstm_statedict_normalized.pt"
STATEDICT_TO_LOAD = "mimo_lstm_statedict.pt"


print("loading logs")
full_logs = []

for log in tqdm(LOGS):
    full_logs.append(torch.load(os.path.join(LOG_FOLDER,log,"logfile.pt")))
topick = ["Thr","Ail","Elev","Rudd","Roll","Pitch",
          "Yaw","Spd","GyrX","GyrY","GyrZ","AccX","AccY","AccZ"]

#full_logs = torch.Tensor(normalize(pd.concat(full_logs)[topick]).values)
full_logs = torch.Tensor(pd.concat(full_logs)[topick].values)

model = MIMOLSTM(input_size=len(topick),lookback=LOOKBACK)
model.load_state_dict(torch.load(
        os.path.join(GIT_ROOT,"XX_logs","statedicts",STATEDICT_TO_LOAD)
))
model.eval()

#skip boring part
SKIP = 2500
plot_bars = False

#heat control
pid = PID(.2,.7,0)
heat = 20
set_temp = 20
heat_queue = deque([],LOOKFORWARD)

for it, _ in enumerate(full_logs, LOOKBACK+SKIP):
    logs_to_look_at = full_logs[-LOOKBACK+it:it,:].unsqueeze(0)
    plt.plot(range(-100,0),logs_to_look_at[0,:,0])
    for i in range(LOOKFORWARD):
        data_pred = model.forward(logs_to_look_at)
        logs_to_look_at = torch.cat(
            [logs_to_look_at[:,1:,:],
             data_pred.unsqueeze(0).unsqueeze(1)],
             dim=1)
    
    
    gt = full_logs[it:it+LOOKFORWARD,0].detach().numpy()
    pred = logs_to_look_at[0,-LOOKFORWARD-2:,0].detach().numpy()
    # control on the most recent point    
    cont_inp = pid.step(set_temp,heat)
    if abs(cont_inp) > 1000:
        print("prevent overflow")
        exit()
    heat += (logs_to_look_at[0,0,0].detach().numpy()*0.3)- cont_inp
    heat_queue.append(heat)

    plt.plot(pred,"red")
    plt.plot(gt,"blue")

    
    plt.plot(range(-len(heat_queue),0),heat_queue,"green")

    plt.axis([-LOOKBACK,LOOKFORWARD-1,0,110])
    plt.title("blue = ground truth; red = prediction; green pid without pred")
    plt.grid(True)
    plt.savefig("pidtest.png")
    plt.clf()
    print(it, end = "\r")
plt.show()