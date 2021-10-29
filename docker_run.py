import pandas as pd 
import os
import pyodbc 
import sqldata as sq
import shutil
import subprocess
import sys 
import random
import platform
# Run All Exported Files
try:    
    PYODBC_Connection, df, sts = sq.import_initialization()
    # Identify the operatings system.   If it's Linux, start with sudo to ensure it runs
    base_cmd = ""    
    if not ("windows" in platform.system().lower()):
        base_cmd = "sudo "    
    if (len(df)>0) and (sts=="SUCCESS"):
        row_1 = df.iloc[0]    
        define_samples_path = row_1["define_samples_path"]
        output_dir_base = row_1["output_dir_base"]
        docker_dir_define_samples = row_1["docker_dir_define_samples"]
        docker_dir = row_1["docker_dir"]
        row_1 = None
        df = None
        files = os.listdir(define_samples_path)
        # Remove the base files
        files.remove("definesample.py")
        files.remove("definesampletemplate.txt")
        for file in files:
            project_name = 'definesample_'
            project_name = file[len(project_name):]
            project_name = project_name[0:len(project_name)-4]
            project_file = project_name + '.blend'
            output_dir_end = output_dir_base + project_name + "/"
            if (os.path.isdir(output_dir_end) == True):            
                shutil.rmtree(output_dir_end)
            os.mkdir(output_dir_end)            
            os.remove(docker_dir_define_samples + 'definesample.py')
            shutil.move(define_samples_path + file, docker_dir_define_samples + 'definesample.py')        
            os.chdir(docker_dir)
            print(docker_dir)
            project_status = 'BLDG'
            sql = f"EXEC [WebSite].[FileNameStatusUpsert] @FileName = '{project_file}', @Status = '{project_status}'"
            sts = sq.run_sql(sql, PYODBC_Connection)
            cmd = 'docker-compose build amagcons_v15_12'
            if not ("windows" in platform.system().lower()):
                cmd = base_cmd + ' ' + cmd             
            returned_value = os.system(cmd)            
            if returned_value ==0:
                ln = int(random.random()*100000)
                print("Starting Docker Run")                
                project_status = 'RUNNING'
                sql = f"EXEC [WebSite].[FileNameStatusUpsert] @FileName = '{project_file}', @Status = '{project_status}'"
                sts = sq.run_sql(sql, PYODBC_Connection)                                
                cmd = 'docker container run -v ' + output_dir_end + ':/output_data --name amagcons_v15_12_' + str(ln) + ' amagcons_v15_12'            
                if not ("windows" in platform.system().lower()):
                    cmd = base_cmd + ' ' + cmd 
                print(cmd)
                returned_value = os.system(cmd)     
                cmd = 'docker rm ' + 'amagcons_v15_12_' + str(ln)                
                if not ("windows" in platform.system().lower()):
                    cmd = base_cmd + ' ' + cmd                 
                project_status = 'FINISHED'
                sql = f"EXEC [WebSite].[FileNameStatusUpsert] @FileName = '{project_file}', @Status = '{project_status}', @ContainerID = '', @ContainerName = ''"
                sts = sq.run_sql(sql, PYODBC_Connection)                                
                returned_value = os.system(cmd)     
    print("SUCCESS")
except Exception as ex:            
    sts = "FAILURE:  " + str(ex)   
    print(sts)