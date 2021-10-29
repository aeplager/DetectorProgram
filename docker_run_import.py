import pandas as pd 
import os
import pyodbc 
import sqldata as sq
import shutil
import subprocess
import sys 
import random
import platform
import sqlalchemy
from sqlalchemy import create_engine, event

# Run All Exported Files
try:
    sts = "FAILURE"
    PYODBC_Connection, df, sts = sq.import_initialization()
    # Identify the operatings system.   If it's Linux, start with sudo to ensure it runs
    base_cmd = ""    
    base_cmd_copy = "copy"
    base_cmd_dir_sep = "//"
    base_cmd_delete = "del"
    if not ("windows" in platform.system().lower()):
        base_cmd = "sudo "    
        base_cmd_copy = "cp"
        base_cmd_delete = "rm"
    # Establish Files for Import
    print(sts)
    if (len(df)>0) and (sts=="SUCCESS"):
        row_1 = df.iloc[0]    
        define_samples_path = row_1["define_samples_path"]
        output_dir_base = row_1["output_dir_base"]
        docker_dir_define_samples = row_1["docker_dir_define_samples"]
        docker_dir = row_1["docker_dir"]        
        sql_alchemy_conn_string, sts = sq.return_sql_alchemy_string(df)
        row_1 = None
        df = None                        
        # Obtain All Importing Files
        sql = 'EXEC [WebSite].[FileImportingFileInfo]'
        df, sts = sq.ret_pandas(sql, PYODBC_Connection)
        for index, row in df.iterrows():                
            # Copy File For Import
            dir_to_copy_from = row["FileName"]
            dir_to_copy_from = dir_to_copy_from.replace(".blend", "")
            loc_separator = dir_to_copy_from.find("_")
            project_id = dir_to_copy_from[:loc_separator]
            project_version_id = dir_to_copy_from[loc_separator+1:]
            dir_import = output_dir_base + dir_to_copy_from + base_cmd_dir_sep                                    
            # Establish Source and Destination Files
            src = dir_import + "ResultsAll.csv"
            dst = dir_import + "import_file.csv"            
            current_status = row["SYSNAME"]
            project_file = row["FileName"]
            # Copy the files
            print(shutil.copyfile(src, dst))                           
            # Import the file into Pandas Dataframe
            df_import = pd.read_csv(dst)
            # Strip the columns of leading and trailing spaces
            for str_col_name in df_import.columns:                
                str_col_name_striped = str_col_name.strip()
                df_import.rename(columns ={str_col_name:str_col_name_striped}, inplace=True)
            # Rename All Fields                
            #print(df_import.dtypes)
            df_import.rename(columns ={'TimeSeconds':'TimeSeconds','TimeHours':'TimeHours','TimePixel':'TimePixel','ScanRegionName':'ScanRegionName','X_nm':'X_nm','Y_nm':'Y_nm','FrameNum':'FrameNum','N':'N','BeamV':'BeamV','BeamSizeX':'BeamSizeX','BeamSizeY':'BeamSizeY','BeamRotAng':'BeamRotAng','thickness':'thickness','energyHist':'energyHist','traj_image':'traj_image','traj_log':'traj_log','BSEf':'BSEf','SEf':'SEf','Xf':'Xf','rotChamber':'rotChamber','Det1_BSEf':'Det1_BSEf','Det1_SEf':'Det1_SEf','Det1_Xf':'Det1_Xf','energyHist.1':'energyHist_1','traj_log.1':'traj_log_1','Det2_BSEf':'Det2_BSEf','Det2_SEf':'Det2_SEf','Det2_Xf':'Det2_Xf'}, inplace=True)
            # Establish Project ID and Project Version ID
            project_id = dir_to_copy_from[:loc_separator]
            project_version_id = dir_to_copy_from[loc_separator+1:]            
            df_import["ProjectID"] = project_id
            df_import["ProjectVersionsID"] = project_version_id

            # Default Extra Fields
            #,'energyHist.2':'energyHist_2','traj_log.2':'traj_log_2'
            df_import["energyHist_2"] = 0.0
            df_import["traj_log_2"] = 0.0
            df_import["PixelNum"] = 1.0
            df_import["energyHist_3"] = 0.0
            df_import["traj_log_3"] = 0.0
            df_import["Det2_Xf"] = 0.0
            df_import["Det2_SEf"] = 0.0
            df_import["Det2_BSEf"] = 0.0 
            df_import["Det3_Xf"] = 0.0
            df_import["Det3_SEf"] = 0.0
            df_import["Det3_BSEf"] = 0.0 
            # Force Numeric to Numbers
            df_import["Det1_BSEf"] = pd.to_numeric(df_import["Det1_BSEf"], errors='coerce')
            df_import["PixelNum"] = pd.to_numeric(df_import["PixelNum"], errors='coerce')
            df_import["TimeSeconds"] = pd.to_numeric(df_import["TimeSeconds"], errors='coerce')
            df_import["TimeHours"] = pd.to_numeric(df_import["TimeHours"], errors='coerce')
            df_import["TimePixel"] = pd.to_numeric(df_import["TimePixel"], errors='coerce')
            df_import["X_nm"] = pd.to_numeric(df_import["X_nm"], errors='coerce')
            df_import["Y_nm"] = pd.to_numeric(df_import["Y_nm"], errors='coerce')
            df_import["FrameNum"] = pd.to_numeric(df_import["FrameNum"], errors='coerce')
            df_import["N"] = pd.to_numeric(df_import["N"], errors='coerce')
            df_import["BeamV"] = pd.to_numeric(df_import["BeamV"], errors='coerce')
            df_import["BeamSizeX"] = pd.to_numeric(df_import["BeamSizeX"], errors='coerce')
            df_import["BeamSizeY"] = pd.to_numeric(df_import["BeamSizeY"], errors='coerce')
            df_import["thickness"] = pd.to_numeric(df_import["thickness"], errors='coerce')
            df_import["BSEf"] = pd.to_numeric(df_import["BSEf"], errors='coerce')
            df_import["SEf"] = pd.to_numeric(df_import["SEf"], errors='coerce')
            df_import["Xf"] = pd.to_numeric(df_import["Xf"], errors='coerce')
            df_import["rotChamber"] = pd.to_numeric(df_import["rotChamber"], errors='coerce')
            df_import["Det1_BSEf"] = pd.to_numeric(df_import["Det1_BSEf"], errors='coerce')
            df_import["Det1_SEf"] = pd.to_numeric(df_import["Det1_SEf"], errors='coerce')
            df_import["Det1_Xf"] = pd.to_numeric(df_import["Det1_Xf"], errors='coerce')
            df_import["Det2_BSEf"] = pd.to_numeric(df_import["Det2_BSEf"], errors='coerce')
            df_import["Det2_SEf"] = pd.to_numeric(df_import["Det2_SEf"], errors='coerce')
            df_import["Det2_Xf"] = pd.to_numeric(df_import["Det2_Xf"], errors='coerce')
            df_import["energyHist_2"] = pd.to_numeric(df_import["energyHist_2"], errors='coerce')
            df_import["traj_log_2"] = pd.to_numeric(df_import["traj_log_2"], errors='coerce')
            df_import["Det3_BSEf"] = pd.to_numeric(df_import["Det3_BSEf"], errors='coerce')
            df_import["Det3_SEf"] = pd.to_numeric(df_import["Det3_SEf"], errors='coerce')
            df_import["Det3_Xf"] = pd.to_numeric(df_import["Det3_Xf"], errors='coerce')
            df_import["energyHist_3"] = pd.to_numeric(df_import["energyHist_3"], errors='coerce')
            df_import["traj_log_3"] = pd.to_numeric(df_import["traj_log_3"], errors='coerce')
            # Replace Any NaN to 0
            df_import.replace('NaN',0)
            # Reorder the Columns
            df_import = df_import[['ProjectID','ProjectVersionsID','PixelNum','TimeSeconds','TimeHours','TimePixel','ScanRegionName','X_nm','Y_nm','FrameNum','N','BeamV','BeamSizeX','BeamSizeY','BeamRotAng','thickness','energyHist','traj_image','traj_log','BSEf','SEf','Xf','rotChamber','Det1_BSEf','Det1_SEf','Det1_Xf','energyHist_1','traj_log_1','Det2_BSEf','Det2_SEf','Det2_Xf','energyHist_2','traj_log_2','Det3_BSEf','Det3_SEf','Det3_Xf','energyHist_3','traj_log_3']]
            # Change the types of Columns to the appropriate field
            #print(df_import["Det1_BSEf"].head())
            df_import["ProjectID"] = df_import["ProjectID"].astype("int")
            df_import["ProjectVersionsID"] = df_import["ProjectVersionsID"].astype("int")
            df_import["PixelNum"] = df_import["PixelNum"].astype("float")
            df_import["TimeSeconds"] = df_import["TimeSeconds"].astype("float")
            df_import["TimeHours"] = df_import["TimeHours"].astype("float")
            df_import["TimePixel"] = df_import["TimePixel"].astype("float")
            df_import["ScanRegionName"] = df_import["ScanRegionName"].astype("str")
            df_import["X_nm"] = df_import["X_nm"].astype("float")
            df_import["Y_nm"] = df_import["Y_nm"].astype("float")
            df_import["FrameNum"] = df_import["FrameNum"].astype("float")
            df_import["N"] = df_import["N"].astype("float")
            df_import["BeamV"] = df_import["BeamV"].astype("float")
            df_import["BeamSizeX"] = df_import["BeamSizeX"].astype("float")
            df_import["BeamSizeY"] = df_import["BeamSizeY"].astype("float")
            df_import["BeamRotAng"] = df_import["BeamRotAng"].astype("str")
            df_import["thickness"] = df_import["thickness"].astype("float")
            df_import["energyHist"] = df_import["energyHist"].astype("str")
            df_import["traj_image"] = df_import["traj_image"].astype("str")
            df_import["traj_log"] = df_import["traj_log"].astype("str")
            df_import["BSEf"] = df_import["BSEf"].astype("float")
            df_import["SEf"] = df_import["SEf"].astype("float")
            df_import["Xf"] = df_import["Xf"].astype("float")
            df_import["rotChamber"] = df_import["rotChamber"].astype("str")
            df_import["Det1_BSEf"] = df_import["Det1_BSEf"].astype("float")
            df_import["Det1_SEf"] = df_import["Det1_SEf"].astype("float")
            df_import["Det1_Xf"] = df_import["Det1_Xf"].astype("float")
            df_import["energyHist_1"] = df_import["energyHist_1"].astype("str")
            df_import["traj_log_1"] = df_import["traj_log_1"].astype("str")
            df_import["Det2_BSEf"] = df_import["Det2_BSEf"].astype("float")
            df_import["Det2_SEf"] = df_import["Det2_SEf"].astype("float")
            df_import["Det2_Xf"] = df_import["Det2_Xf"].astype("float")
            df_import["energyHist_2"] = df_import["energyHist_2"].astype("float")
            df_import["traj_log_2"] = df_import["traj_log_2"].astype("float")
            df_import["Det3_BSEf"] = df_import["Det3_BSEf"].astype("float")
            df_import["Det3_SEf"] = df_import["Det3_SEf"].astype("float")
            df_import["Det3_Xf"] = df_import["Det3_Xf"].astype("float")
            df_import["energyHist_3"] = df_import["energyHist_3"].astype("float")
            df_import["traj_log_3"] = df_import["traj_log_3"].astype("float")
            sql = f"EXEC [WebSite].[TrajectoryDelete] @ProjectID = {project_id}, @ProjectVersionID = {project_version_id}"
            sts = sq.run_sql(sql, PYODBC_Connection)
            # Fast Push of Data to the Database
            print(sql_alchemy_conn_string)
            eng = sqlalchemy.create_engine(sql_alchemy_conn_string)
            @event.listens_for(eng, "before_cursor_execute")
            def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
                if executemany:
                    cursor.fast_executemany = True
            df_import.to_sql('TrajectoryData', eng, index=False, if_exists="append", schema="WebSite")   


            if (current_status=="FINISHED"):
                current_status = "FINALIZED"
                sql = f"EXEC [WebSite].[FileNameStatusUpsert] @FileName = '{project_file}', @Status = '{current_status}', @ContainerID = '', @ContainerName = ''"
                sts = sq.run_sql(sql, PYODBC_Connection)                                

    sts = "SUCCESS"
    print(sts)
except Exception as ex:            
    sts = "FAILURE:  " + str(ex)   
    print(sts)