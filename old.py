# Imports
import os
import pandas as pd
import pyodbc
import psutil
import shutil
import signal
import sqldata as sq
import subprocess
import os
import time

def return_file_names(process):
    try:
        file_name = process.cmdline () 
        return "SUCCESS", file_names
    except Exception as ex:       
        return "FAILURE: " + str(ex), None
    
def return_user_name(process):
    try:
        username = process.username () 
        return "SUCCESS", username
    except Exception as ex:       
        return "FAILURE: " + str(ex), None
try:
    # Establish Commands
    # Base Command to Launch Application
    # base_cmd = 'export DISPLAY=:10.0 && nohup /snap/blender/624/blender '
    # #base_cmd = 'export DISPLAY=:10.0 && disown -h /snap/blender/624/blender '
    # # Base Directory for Blender Files
    # base_directory = "/home/aeplager/Documents/BlenderFiles/"
    
    # print("Printed immediately.")
    # Initial Set Up
    PYODBC_Connection, df, sts = sq.import_initialization()
    if (sts == "SUCCESS") and (len(df)>0):
        row_1 = df.iloc[0]    
        base_directory = row_1["base_directory"]
        base_cmd = row_1["base_cmd"]
        base_file = row_1["base_file"]
        #base_directory= row_1["base_directory"]
        #base_file = 'base_file.blend'
        for i_round in range(1,2,):
            print("Starting round " + str(i_round))        
            # Connection to Database
            sql = f"EXEC [WebSite].[FileMaxGetInfo]"
            df, sts = sq.ret_pandas(sql)
            sts = "SUCCESS"
            ln = len(df)
            base_launch = 0
            if (ln==0):
                # No Records
                print("FAILURE")
            else:
                row_1 = df.iloc[0]        
                launch_file = row_1["FileName"]
                # Detect if Launch File exists
                if os.path.isfile(base_directory + launch_file) == False:
                    base_launch=1
                    src = base_directory + base_file
                    dst = base_directory + launch_file 
                    print(shutil.copyfile(src, dst))        
                print(launch_file)
                c = 0
                detect_file_open = 0
                blender_not_open = 0
                for process in psutil.process_iter ():
                    c=c+1        
                    Name = process.name () # Name of the process
                    ID = process.pid # ID of the process
                    #user_name = process.username ()
                    sts_user_name, user_name = return_user_name(process)                    
                    sts_file_name, file_names = return_file_names(process)                    
                    #file_names = process.cmdline ()                                  
                    if (Name == "blender") and (sts_user_name=="SUCCESS") and (sts_user_name=="SUCCESS"):
                        blender_not_open = 1
                        print("FOUND BLENDER")
                        print(file_names)
                        ln_files = len(file_names)                
                        if (ln_files==1):
                            # Kill the Proccess because this process has nothing open
                            print("KILL PROCESS - POSITION 1")
                            os.kill(int(ID), signal.SIGKILL)
                        else:
                            # Test if file name is the same
                            file_name = file_names[1]
                            print("File Name = " + file_name)
                            print("Launch File = " + base_directory + launch_file)
                            if (file_name == base_directory + launch_file):
                                # Do Not Launch
                                detect_file_open = 1
                                print("File Already Open")
                            else:
                                # Kill the Proccess
                                print("KILL PROCESS - POSITION 2")
                                os.kill(int(ID), signal.SIGKILL)
                
                if (detect_file_open == 0) or (blender_not_open == 0):
                    print("Opening Files")
                    base_cmd = str(base_cmd)
                    if (len(base_cmd.strip())>1) and (base_cmd.lower() !='nan'):
                        os.system(base_cmd + base_directory + launch_file) 
                    else:
                        os.system(base_directory  + launch_file)
                    i_round=20
                    break
                print("detect_file_open = " + str(detect_file_open))
                print("base_launch = " + str(base_launch))
                print("Number of Processes = " + str(c))
                print("SUCCESS")
                if (i_round <= 8):                
                    time.sleep(4)
                    print("Rounds Run " + str(i_round))
                else:
                    break
except Exception as ex:            
    sts = "FAILURE-" + str(ex)
    print(sts)

