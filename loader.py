import os
import torch
import pandas as pd
from utilities import get_git_root
from tqdm import tqdm

class Loader:
    def __init__(self, to_pick) -> None:
        self.logs = None
        self.to_pick = to_pick
        self.GIT_ROOT = get_git_root()
        self.logs = os.listdir(os.path.join(self.GIT_ROOT,"XX_logs","logs"))
        self.paths = [
            os.path.join(self.GIT_ROOT,"XX_logs","logs",x,"logfile.pt") for x in self.logs
        ]

    def load(self) -> torch.Tensor:
        logs = []
        print("Loader: loading logs")
        for path in tqdm(self.paths):
            logs.append(torch.load(path))
        self.logs = pd.concat(logs)
        self.logs = self.logs[self.to_pick]
        return torch.Tensor(self.logs.values)
