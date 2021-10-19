import pandas as pd 
import os
import pyodbc 
import sqldata as sq
import shutil
import subprocess
import sys 
import random
# Location of Define Samples Files
# /home/aeplager/Documents/define_samples_scripts/
define_samples_path = '/home/aeplager/Documents/define_samples_scripts/'
output_dir_base = '/home/aeplager/Documents/DockerData/'
docker_dir_define_samples = '/home/aeplager/Documents/Docker/DockerRealNew/amagcons/JMONSEL/'
docker_dir = '/home/aeplager/Documents/Docker/DockerRealNew/'
Driver = '{ODBC Driver 17 for SQL Server}'
Server = 'localhost'
Database = 'amagcons'
Pwd = 'amagcons_vm#12'
Uid = 'sa'
# Password check   
PYODBC_Connection = 'DRIVER=' + Driver + ';SERVER=' + Server +  ';DATABASE=' + Database + ';UID=' + Uid + ';PWD=' + Pwd + ";Encrypt=yes;TrustServerCertificate=yes"
files = os.listdir(define_samples_path)
print("Position 1")
for f in files:
    print("Position 2")
    if (f != 'definesample.py') and (f != 'definesampletemplate.txt'):
        print(f)           
        file_name = f
        project_name = 'definesample_'
        project_name = f[len(project_name):]
        project_name = project_name[0:len(project_name)-4]
        output_dir_end = output_dir_base + project_name + "/"
        docker_dir = '/home/aeplager/Documents/Docker/DockerRealNew/'
        print("Position 3")
        print(project_name)
        # Set up Base Directory
        if (os.path.isdir(output_dir_end) == True):            
            shutil.rmtree(output_dir_end)
        os.mkdir(output_dir_end)
        print("Position 4")
        # Remove Define Samples File
        #print(docker_dir_define_samples + )
        os.remove(docker_dir_define_samples + 'definesample.py')
        shutil.move(define_samples_path + f, docker_dir_define_samples + 'definesample.py')
        print("Position 5")
        os.chdir(docker_dir)
        cmd = 'docker-compose build amagcons_v15_12'        
        print(cmd)
        returned_value = os.system(cmd)
        print(str(returned_value))
        if returned_value ==0:
            ln = int(random.random()*100000)
            print("Starting Docker Run")
            cmd = 'docker container run -v ' + output_dir_end + ':/output_data --name amagcons_v15_12_' + str(ln) + ' amagcons_v15_12'            
            print(cmd)
            returned_value = os.system(cmd)
            if (returned_value == 0):
                print("SUCCESS")
                # Run Import Into Tables
                results_csv = output_dir_end + 'ResultsAll.csv'
                cnxn = pyodbc.connect(PYODBC_Connection)
                #project_name = 'test'
                sql = "SELECT * FROM [WebSite].[Projects] WHERE [ProjectName] = '" + project_name + "'"
                df_project = pd.read_sql(sql, cnxn)                
                cnxn.commit()
                ln = len(df_project)
                if (ln == 0):
                    sql = "INSERT INTO [WebSite].[Projects] ([ProjectName]) VALUES ('" + project_name + "')"    
                    cursor = cnxn.cursor()            
                    cursor.execute(sql)
                    cnxn.commit()          
                sql = "SELECT * FROM [WebSite].[Projects] WHERE [ProjectName] = '" + project_name + "'"
                df_project = pd.read_sql(sql, cnxn)                
                cnxn.commit()
                project_id = df_project.loc[0][0]  
                cursor = cnxn.cursor()            
                sql = 'DELETE FROM [WebSite].[TrajectoryData] WHERE [ProjectID] = ' + str(project_id)
                cursor.execute(sql)
                cnxn.commit()
                cnxn.close()  
                df_results = pd.read_csv(results_csv, skipinitialspace = True)
                df_results = df_results.rename(columns = {'energyHist.1':'energyHist_1', 'traj_log.1':'traj_log_1', 'None.1': 'None_1'})
                del df_results['None']
                del df_results['None_1']
                cnxn = pyodbc.connect(PYODBC_Connection)
                cursor = cnxn.cursor()
                for index, row in df_results.iterrows():    
                    sql = "INSERT INTO [WebSite].[TrajectoryData] ([ProjectID],[PixelNum], [TimeSeconds], [TimeHours], [TimePixel], [ScanRegionName], [X_nm], [Y_nm], [FrameNum], [N], [BeamV], [BeamSizeX], [BeamSizeY], [BeamRotAng], [thickness], [energyHist], [traj_image], [traj_log], [BSEf], [SEf], [Xf], [rotChamber])"
                    sql = sql + " VALUES("
                    sql = sql + str(project_id) 
                    sql = sql + ", " + str(row.PixelNum)
                    sql = sql + ", " + str(row.TimeSeconds)
                    sql = sql + "," + str(row.TimeHours)
                    sql = sql + "," + str(row.TimePixel)
                    sql = sql + "," + "'" + str(row.ScanRegionName) + "'"
                    sql = sql + "," + str(row.X_nm)
                    sql = sql + "," + str(row.Y_nm)
                    sql = sql + "," + str(row.FrameNum)
                    sql = sql + "," + str(row.N)
                    sql = sql + "," + str(row.BeamV)
                    sql = sql + "," + str(row.BeamSizeX)
                    sql = sql + "," + str(row.BeamSizeY)
                    sql = sql + "," + "'" + str(row.BeamRotAng) + "'"
                    sql = sql + "," + str(row.thickness)
                    sql = sql + "," + "'" + str(row.energyHist) + "'"
                    sql = sql + "," + "'" + str(row.traj_image) + "'"#   
                    sql = sql + "," + "'" +  str(row.traj_log) + "'"
                    sql = sql + "," + str(row.BSEf)
                    sql = sql + "," + str(row.SEf)
                    sql = sql + "," + str(row.Xf)
                    sql = sql + "," + "'" + str(row.rotChamber) + "'"
                    sql = sql + ")"
                    #print(sql)
                    cursor.execute(sql)
                    #break
                cnxn.commit()
                cursor.close()                                

            else:
                print("FAILURE")
        print('Finished')



