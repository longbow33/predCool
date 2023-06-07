import os
from collections import deque
import torch
import pandas as pd
import matplotlib.pyplot as plt

from loader import Loader
from model import SISOLSTM
from utilities import prepare_data, get_git_root

# Hyperparameters
LOOKBACK = 1000
LOOKFORWARD = 30
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
GIT_ROOT = get_git_root()
LOG_FOLDER = os.path.join(GIT_ROOT,"XX_logs","logs")
LOGS = [x for x in os.listdir(LOG_FOLDER)]

# Inits
model = SISOLSTM(input_size = LOOKBACK)
loaders = [Loader(x) for x in [32,35,36]]

# Loading
full_logs = [torch.load(os.path.join(LOG_FOLDER,log,"logfile.pt")) for log in LOGS]

full_logs = pd.concat(full_logs)
all_logs = full_logs["Thr"]

prepped_data = prepare_data(all_logs,LOOKBACK)

model.load_state_dict(torch.load(
        os.path.join(loaders[0].general_statedictpath,
                 "siso_lstm_statedict.pt"),
        map_location=DEVICE
        )
    )

model.eval()
all_logs = all_logs.values


# skip boring part of flight
SKIP = 2000
plot_gps = False

# Predicting and Plotting
for it, _ in enumerate(all_logs,LOOKBACK+SKIP):
    #print(it)
    thr_gt = all_logs[-LOOKBACK+it:LOOKFORWARD+it]
    thr_to_pred_on = prepped_data[it]
    thr_to_pred_on = deque([float(x) for x in thr_to_pred_on],maxlen=LOOKBACK)
    for i in range(LOOKFORWARD):
        thr_to_pred_on_tens = torch.Tensor(thr_to_pred_on)
        forw = model.forward(thr_to_pred_on_tens.unsqueeze(0))
        thr_to_pred_on.append(float(forw))
    
    # plot predictions
    if plot_gps:
        plt.subplot(2,1,1)
    plt.plot(range(LOOKFORWARD+1),thr_gt[-LOOKFORWARD-1:],"blue")
    plt.plot(range(LOOKFORWARD+1),list(thr_to_pred_on)[-LOOKFORWARD-1:],"red")
    plt.axis([0,LOOKFORWARD,0,110])
    plt.title("Blue -> Ground Truth, Red -> Prediction")
    plt.ylabel("% Thrust")
    plt.xlabel("Timesteps")

    # plot gps
    if plot_gps:
        plt.subplot(2,1,2)
        plt.plot(full_logs["Lat"][:it-LOOKBACK],full_logs["Lng"][:it-LOOKBACK])
    
    plt.pause(.01)
    plt.clf()
    plt.grid(True)
    print(it,end="\r")
plt.show()

# acceptable, must be improved