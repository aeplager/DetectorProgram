import pyodbc
import pandas as pd 
import json
import os
#import api_general as ap
import requests 
import sqlalchemy
import platform
from sqlalchemy import create_engine, event

def connect_db(PYODBC_Connection):
    try:
        #PYODBC_Connection, df, sts = import_initialization()        
        cnxn = pyodbc.connect(PYODBC_Connection)                
        sts = "SUCCESS"
        return cnxn, sts
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)                    
        return None, sts
def ret_pandas(sql, PYODBC_Connection):
    try:
        cnxn, sts = connect_db(PYODBC_Connection)   
        df = pd.read_sql(sql, cnxn)                          
        cnxn.commit()
        cnxn.close()        
        return df, "SUCCESS"
    except Exception as ex:                    
        return None, "FAILURE:  " + str(ex)        
def ret_json(sql, PYODBC_Connection):
    try:        
        data, sts = ret_pandas(sql, PYODBC_Connection)
        if (sts == "SUCCESS"):
            jsonstring = data.to_json(orient='index')
        else:
            sts = "FAILURE"
            jsonstring = None
        return jsonstring, sts          
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)        
        return None, sts   
def run_sql(sql, PYODBC_Connection):
    try:        
        #PYODBC_Connection, df, sts = import_initialization()        
        conn = pyodbc.connect(PYODBC_Connection)
        #conn, sts = connect_db()
        cursor = conn.cursor()
        cursor.execute(sql)
        cursor.close()
        conn.commit()    #return_value = os.system(cmd)  
        conn.close()
        sts="SUCCESS"        
        return sts 
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)        
        return sts   

def import_initialization():    
    try:
        path = script = os.path.realpath(__file__)
        path = os.path.realpath(__file__)
        separator = "\\"
        source_file_name = "InitializationFileWindows.csv"
        if not ("windows" in platform.system().lower()):
            separator = "/"
            source_file_name = "InitializationFileUbuntu.csv"
        iloc = len(path)
        iloc = path.rfind(separator,0, iloc)
        path = path[:iloc] + separator + source_file_name
        #print("Script path:", path)
        #path = "/home/amagcons/Documents/BlenderFiles/PCScripts/InitializationFile.csv" 
        #df = pd.read_csv(r'InitializationFile.csv')        
        df = pd.read_csv(path)
        ln = len(df)
        if (ln>0):
            row_1 = df.iloc[0]
            Driver = row_1.Driver
            Server = row_1.Server
            Database = row_1.Database
            Pwd = row_1.Pwd
            Uid = row_1.Uid
            AdditionalCommands = row_1.AdditionalCommands
            UseServer = row_1.UseServer
            UseServer = UseServer.upper().strip()        
            if (UseServer=="YES"):
                myip = requests.get('https://www.wikipedia.org').headers['X-Client-IP']
                Server = str(myip)
            PYODBC_Connection = 'DRIVER=' + Driver + ';SERVER=' + Server +  ';DATABASE=' + Database + ';UID=' + Uid + ';PWD=' + Pwd + ";" + AdditionalCommands
            # New Command Entered
            sts = "SUCCESS" 
        return PYODBC_Connection, df, sts
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)   
        return None, None, sts

def return_sql_alchemy_string(df):
    try:
        ln = len(df)
        if (ln>0):
            row_1 = df.iloc[0]
            Driver = row_1.Driver
            Driver = Driver.replace("{","").replace("}","")
            Server = row_1.Server
            Server = Server.replace(",1433","").replace(", 1433","")            
            UseServer = row_1.UseServer
            UseServer = UseServer.upper().strip()        
            if (UseServer=="YES"):
                myip = requests.get('https://www.wikipedia.org').headers['X-Client-IP']
                Server = str(myip)            
            Database = row_1.Database
            Pwd = row_1.Pwd
            Uid = row_1.Uid            
            conn_string = "mssql+pyodbc://" + Uid + ":" + Pwd + "@" + Server + ":1433/" + Database + "?driver=" + Driver
            sts = "SUCCESS"
        else:
            sts = "FAILURE"
        return conn_string, sts
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)   
        return None, sts          