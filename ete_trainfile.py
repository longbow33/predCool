import os
import torch
from torch import nn

from loader import Loader
from model import MIMOLSTM
from electric_motor import Motor

# HYPERPARAMETERS
LR = 0.001
EPOCHS = 2000
LOOKBACK = 100

attributes_to_pick = ["Thr","Ail","Elev","Rudd","Roll","Pitch",
          "Yaw","Spd","GyrX","GyrY","GyrZ","AccX","AccY","AccZ"]
loader = Loader(attributes_to_pick)
logs = loader.load()

# initiate device to train on
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"device is {DEVICE}")

# define electric Motor simulation
motor = Motor(20,100)


# define model, optimizer and loss
model = MIMOLSTM(input_size=len(attributes_to_pick),lookback=LOOKBACK)
optimizer = torch.optim.Adam(params=model.parameters(),lr = LR)
loss_fn = nn.MSELoss()

print(logs.shape)

