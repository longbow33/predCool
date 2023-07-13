import os
import git
from pathlib import Path
import re

cwd = os.getcwd()
git_root = git.Repo(cwd,search_parent_directories= True)
git_root = Path(git_root.git.rev_parse("--show-toplevel"))
mavlogdump_path = os.path.join(git_root,"loghandling")

log_types = ["AETR","AHR2","GPS","IMU"]

log_files = os.listdir(os.path.join(git_root,"XX_logs","logs_to_add"))
print(log_files)

for log_file in log_files:
    ## check if logfile.xslx present
    if os.path.exists(os.path.join(git_root,"XX_logs","logs",log_file,"logfile.xslx")):
        continue
    ## ^ not tested
    try:
        num = re.search(r"\d+",log_file)[0]
        print(num)
    # if num is none, skip 
    except:
        continue

    for log_type in log_types:
        
        mld = os.path.join(mavlogdump_path,"mavlogdump.py")
        type_declaration = " --types "+log_type
        format_declaration = " --format csv "
        output_declaration = " >> "+os.path.join(git_root,"XX_logs","logs",str(num),str(log_type+".csv "))
        log_location = os.path.join(git_root,"XX_logs","logs_to_add",log_file)

        if not os.path.exists(os.path.join(git_root,"XX_logs","logs",num)):
            os.makedirs(os.path.join(git_root,"XX_logs","logs",num))

        run_str = "python3 "+ str(mld) + type_declaration + format_declaration + log_location + output_declaration
        print(run_str)
        os.system(run_str)
    os.rename(os.path.join(git_root,"XX_logs","logs_to_add",log_file),os.path.join(git_root,"XX_logs","logs_to_add","done",log_file))