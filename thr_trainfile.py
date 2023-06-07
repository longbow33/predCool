import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

from loader import Loader
from utilities import prepare_data, get_git_root, plot_losses
from model import SISOLSTM

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
EPOCHS = 200
LR = 0.00001
LOOKBACK = 1000 #was 100
GIT_ROOT = get_git_root()
LOG_FOLDER = os.path.join(GIT_ROOT,"XX_logs","logs")
LOGS = [x for x in os.listdir(LOG_FOLDER)]

print("loading logs")
full_logs = []
for log in tqdm(LOGS):
    full_logs.append(torch.load(os.path.join(LOG_FOLDER,log,"logfile.pt")))

print("concatenating")
full_logs = pd.concat(full_logs)

topick = ["Thr"]
all_logs = full_logs[topick]

# loading and filtering done
# now prepare the data -> use lookback function
prepped_data = prepare_data(all_logs,LOOKBACK).to(DEVICE)

dl = DataLoader(prepped_data,
                batch_size= 1000,
                shuffle= True)

model = SISOLSTM(input_size= LOOKBACK).to(DEVICE)
optimizer = torch.optim.Adam(params=model.parameters(),
                             lr = LR)
loss_fn = nn.MSELoss()

print("starting Training\n--------------")
losses = []

for epoch in tqdm(range(EPOCHS)):
    model.train()

    for batch in dl:
        #batch.shape = batchsize, lookback
        optimizer.zero_grad()
        thr_pred = model.forward(batch[:,:-1])
        thr_true = batch[:,-1:]
        loss = loss_fn(thr_pred,thr_true)
        loss.backward()
        optimizer.step()
    
    if epoch % 10 == 0:
        model.eval()
        print(f"Epoch: {epoch} | Loss {loss}")
    
    losses.append(loss.item())

    plt.plot(losses,"red")
    plt.axis([0,len(losses)-1,0,max(losses)])
    plt.savefig("siso_loss_curve.png")

torch.save(model.state_dict(),
           os.path.join(GIT_ROOT,"XX_logs","statedicts",
                        "siso_lstm_statedict.pt")
            )

print("done and saved")
