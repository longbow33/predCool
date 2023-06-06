import os
import git
from pathlib import Path

cwd = os.getcwd()
git_root = git.Repo(cwd,search_parent_directories= True)
git_root = Path(git_root.git.rev_parse("--show-toplevel"))

datacombiner_path = os.path.join(git_root,"02_first_model","datacombiner.py")

log_folder = os.path.join(git_root,"XX_logs","logs")
folders = os.listdir(log_folder)
print(folders)

for folder in folders:

    run_str = "python3 "+ str(datacombiner_path) + " --log "+str(folder)
    print(run_str)
    os.system(run_str)
