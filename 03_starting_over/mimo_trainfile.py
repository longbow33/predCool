import os
import torch
from torch import nn

import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import random

from utilities import get_git_root
from model import MIMOLSTM

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"device is {DEVICE}")
EPOCHS = 200
LR = 0.0001 #second training LR from 0.001 to 0.0001
LOOKBACK = 100
GIT_ROOT = get_git_root()
LOG_FOLDER = os.path.join(GIT_ROOT,"XX_logs","logs")
LOGS = [x for x in os.listdir(LOG_FOLDER)]
BATCHSIZE = 2000



print("loading logs")
full_logs = []
# seems like there is too much data in memory, load one after another?
for log in tqdm(LOGS):
    full_logs.append(torch.load(os.path.join(LOG_FOLDER,log,"logfile.pt")))

topick = ["Thr","Ail","Elev","Rudd","Roll","Pitch",
          "Yaw","Spd","GyrX","GyrY","GyrZ","AccX","AccY","AccZ"]

model = MIMOLSTM(input_size=len(topick),lookback=LOOKBACK).to(DEVICE)
model.load_state_dict(
    torch.load(os.path.join(GIT_ROOT,"XX_logs","statedicts","mimo_lstm_statedict.pt"))
)
optimizer = torch.optim.Adam(params=model.parameters(),
                             lr = LR)
loss_fn = nn.MSELoss()

full_logs = torch.Tensor(pd.concat(full_logs)[topick].values).to(DEVICE)
    
losses = []


for epoch in tqdm(range(EPOCHS)):

    model.train()
    
    places_to_look_at = list(range(LOOKBACK,full_logs.shape[0]-1))
    places = random.sample(places_to_look_at,len(places_to_look_at))
    batches = [places[b:b+BATCHSIZE] for b in range(0,len(places),BATCHSIZE)]
    
    for batch in batches:
        data_to_pred_on = torch.stack(
            [full_logs[-LOOKBACK+place:place,:] for place in batch],1).swapaxes(1,0)
        data_ground_truth = torch.stack(
            [full_logs[place,:] for place in batch],0)
        optimizer.zero_grad()
        data_pred = model.forward(data_to_pred_on)
        #print(data_pred.shape,data_ground_truth.shape)
        loss = loss_fn(data_pred,data_ground_truth)
        loss.backward()
        optimizer.step()

    if epoch % 10 == 0:
        model.eval()
        print(f"Epoch: {epoch} | Loss {loss}")

    losses.append(loss.item())
    plt.title("Losses")
    plt.plot(losses,"red")
    plt.axis([0,max(len(losses)-1,1),0,max(losses)])
    plt.grid(True)
    plt.savefig("mimo_loss_curve.png")

    plt.clf()
    if len(losses) > 20:
        try:
            plt.title("Last 20 Losses")
            plt.plot(losses[-20:],"red")
            plt.axis([0,19,0,max(losses[-20:])])
            plt.grid(True)
            plt.savefig("last_20_mimo_loss_curve.png")
            plt.clf()
        except:
            print("not able to plot last 20")
torch.save(model.state_dict(),
           os.path.join(GIT_ROOT,"XX_logs","statedicts",
                        "mimo_lstm_statedict.pt")
            )
torch.save(losses,os.path.join(GIT_ROOT,"mimo_losses.pt"))
print("done and saved")
