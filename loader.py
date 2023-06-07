"""
This Module ensures the loading of the file is handeled.
"""

import os
import time
from pathlib import Path
import pandas as pd
import git
import torch



class Loader():
    def __init__(self, lognum) -> None:
        self.lognum = str(lognum)
        cwd = os.getcwd()
        git_root = git.Repo(cwd,search_parent_directories= True)
        self.git_root = Path(git_root.git.rev_parse("--show-toplevel"))
        self.logpath = os.path.join(self.git_root,"XX_logs","logs",self.lognum)
        self.logfilepath = os.path.join(self.logpath,"logfile.xlsx")
        self.tensor_savepath = os.path.join(self.logpath,"data.pt")
        self.statedictpath = os.path.join(self.logpath,"statedict.pt")
        self.general_logfolder = os.path.join(self.git_root,"XX_logs","logs")
        self.general_statedictpath = os.path.join(self.git_root,"XX_logs","statedicts")

    def load(self,num_rows=None) -> pd.DataFrame:
        # TODO implement loading from .pt file (faster)
        starttime = time.time()
        print("Loader", self.lognum,": loading database",flush= True)
        try:
            full_data = pd.read_excel(self.logfilepath,index_col=0,nrows=num_rows)
        except FileNotFoundError:
            print("logfile not found, check it is in the right directory")
            exit()
        dtime = time.time()-starttime
        print("Loader: loading complete",flush= True)
        print("Loader: Time elapsed: ",end="")
        print(dtime,flush=True)
        return full_data

    def save_tensor(self,data):
        torch.save(data,self.tensor_savepath)

    def load_tensor(self) -> torch.Tensor:
        return torch.load(self.tensor_savepath)
    
    def save_statedict(self,statedict):
        torch.save(statedict,self.statedictpath)


if __name__ == "__main__":
    git_repo = git.Repo(os.getcwd(),search_parent_directories= True)
    git_root = git_repo.working_tree_dir
    loader = Loader(32)
