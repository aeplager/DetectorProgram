# Imports
import os
import pandas as pd
import pyodbc
import psutil
import shutil
import signal

#import os.path
#import subprocess
##from subprocess import Popen, PIPE
#from subprocess import check_output


# Base Command to Launch Application
base_cmd = 'export DISPLAY=:10.0 && nohup /snap/blender/624/blender '
# Base Directory for Blender Files
base_directory = "/home/aeplager/Documents/BlenderFiles/"
base_file = 'base_file.blend'
import os
import time
print("Printed immediately.")
try:
    for i_round in range(1,10):
        print("Starting round " + str(i_round))        
        # Connection to Database
        sql = f"EXEC [WebSite].[FileMaxGetInfo]"
        sts = "FAILURE"
        Driver = '{ODBC Driver 17 for SQL Server}'
        Server = 'localhost'
        Database = 'amagcons'
        Pwd = 'amagcons_vm#12'
        Uid = 'sa'
        PYODBC_Connection = 'DRIVER=' + Driver + ';SERVER=' + Server +  ';DATABASE=' + Database + ';UID=' + Uid + ';PWD=' + Pwd + ";Encrypt=yes;TrustServerCertificate=yes"
        cnxn = pyodbc.connect(PYODBC_Connection)
        df = pd.read_sql(sql, cnxn)
        cnxn.commit()
        cnxn.close()    
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
                user_name = process.username ()
                file_names = process.cmdline ()              
                if (Name == "blender"):
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
                os.system(base_cmd + base_directory + launch_file)
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