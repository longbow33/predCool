import os
import torch
from torch import nn
from itertools import chain

import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import random

from utilities import get_git_root, normalize, pick_places
from model import MIMOLSTM

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"device is {DEVICE}")
EPOCHS = 20000
LR = 0.0001 #second training LR from 0.001 to 0.0001
LOOKBACK = 100
GIT_ROOT = get_git_root()
LOG_FOLDER = os.path.join(GIT_ROOT,"XX_logs","logs")
LOGS = [x for x in os.listdir(LOG_FOLDER)]
BATCHSIZE = 2000

use_pretrained = False

print("loading logs")
full_logs = []
# seems like there is too much data in memory, load one after another?
for log in tqdm(LOGS):
    full_logs.append(torch.load(os.path.join(LOG_FOLDER,log,"logfile.pt")))

topick = ["Thr","Ail","Elev","Rudd","Roll","Pitch",
          "Yaw","Spd","GyrX","GyrY","GyrZ","AccX","AccY","AccZ"]

model = MIMOLSTM(input_size=len(topick),lookback=LOOKBACK).to(DEVICE)
if use_pretrained:
    model.load_state_dict(
        torch.load(os.path.join(GIT_ROOT,"XX_logs","statedicts","mimo_lstm_statedict.pt"))
    )
optimizer = torch.optim.Adam(params=model.parameters(),
                             lr = LR)
loss_fn = nn.MSELoss()

full_logs = torch.Tensor(normalize(pd.concat(full_logs)[topick]).values).to(DEVICE)
    
losses = []

places_sorted = pick_places(full_logs,LOOKBACK,100)
print(len(places_sorted[0]))
entries_per = 10

for epoch in tqdm(range(EPOCHS)):

    model.train()
    places = [0]
    while min(places) < LOOKBACK:
        places = [random.sample(places_sorted[x],entries_per) for x in range(101)]
        places = list(chain(*places))
    try:
        data_to_pred_on = torch.stack(
            [full_logs[-LOOKBACK+place:place,:] for place in places],1).swapaxes(1,0)
    except RuntimeError as e:
        print(e,min(places),max(places))
        exit()
    data_ground_truth = torch.stack(
        [full_logs[place,:] for place in chain(places)],0)
    optimizer.zero_grad()
    data_pred = model.forward(data_to_pred_on)
    #print(data_pred.shape,data_ground_truth.shape)
    loss = loss_fn(data_pred,data_ground_truth)
    loss.backward()
    optimizer.step()

    if epoch % (EPOCHS/10) == 0:
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
                        "mimo_lstm_statedict_normalized.pt")
            )
torch.save(losses,os.path.join(GIT_ROOT,"mimo_losses_normalized.pt"))
print("done and saved")
