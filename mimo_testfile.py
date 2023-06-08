import os
import torch

import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

from utilities import get_git_root
from model import MIMOLSTM

LOOKBACK = 100
LOOKFORWARD = 100
GIT_ROOT = get_git_root()
LOG_FOLDER = os.path.join(GIT_ROOT,"XX_logs","logs")
LOGS = os.listdir(LOG_FOLDER)


print("loading logs")
full_logs = []

for log in tqdm(LOGS):
    full_logs.append(torch.load(os.path.join(LOG_FOLDER,log,"logfile.pt")))
topick = ["Thr","Ail","Elev","Rudd","Roll","Pitch",
          "Yaw","Spd","GyrX","GyrY","GyrZ","AccX","AccY","AccZ"]

full_logs = torch.Tensor(pd.concat(full_logs)[topick].values)

model = MIMOLSTM(input_size=len(topick),lookback=LOOKBACK)
model.load_state_dict(torch.load(
        os.path.join(GIT_ROOT,"XX_logs","statedicts","mimo_lstm_statedict_normalized.pt")
))
model.eval()

#skip boring part
SKIP = 3000
plot_bars = False

for it, _ in enumerate(full_logs, LOOKBACK+SKIP):
    logs_to_look_at = full_logs[-LOOKBACK+it:it,:].unsqueeze(0)
    for i in range(LOOKFORWARD):
        data_pred = model.forward(logs_to_look_at)
        logs_to_look_at = torch.cat(
            [logs_to_look_at[:,1:,:],
             data_pred.unsqueeze(0).unsqueeze(1)],
             dim=1)
    
    
    plt.plot(logs_to_look_at[0,-LOOKFORWARD:,0].detach().numpy(),"red")
    plt.plot(full_logs[it:it+LOOKFORWARD,0].detach().numpy(),"blue")
    if plot_bars:
        top, bot = sorted([full_logs[it,0].detach().numpy(),
            full_logs[it+LOOKFORWARD,0].detach().numpy()])
        top -= bot
        plt.bar(10,top, bottom = bot, width=10,color = "blue")
        top, bot = sorted([logs_to_look_at[0,-LOOKFORWARD,0].detach().numpy(),
                        logs_to_look_at[0,-1,0].detach().numpy()])
        top -= bot
        plt.bar(20, top, bottom= bot, width= 10, color = "red")
    plt.axis([0,LOOKFORWARD-1,0,110])
    plt.title("blue = ground truth; red = prediction")
    plt.grid(True)
    plt.pause(.01)
    plt.clf()
    print(it,logs_to_look_at[0,0,0], end = "\r")
plt.show()