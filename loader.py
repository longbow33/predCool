"""
this module contains the loader class to handle
the loading of the logfiles
"""

import os
import torch
import pandas as pd
from tqdm import tqdm

from utilities import get_git_root

class Loader:
    """
    the loader class handle the loading of the logfiles
    inputs:
        to_pick:    the attributes to keep while discarding the unnecessary ones.
    returns:
        loader
    """
    def __init__(self, to_pick) -> None:
        self.logs = None
        self.to_pick = to_pick
        self.git_root = get_git_root()
        self.logs = os.listdir(os.path.join(self.git_root,"XX_logs","logs"))
        self.paths = [
            os.path.join(self.git_root,"XX_logs","logs",x,"logfile.pt") for x in self.logs
        ]

    def load(self) -> torch.Tensor:
        """
        loads all logfiles in the given folder.
        returns:
            logfiles:   a torch Tensor containing all the data.
        """
        logs = []
        print("Loader: loading logs")
        for path in tqdm(self.paths):
            logs.append(torch.load(path))
        self.logs = pd.concat(logs)[self.to_pick]
        return torch.Tensor(self.logs.values)
