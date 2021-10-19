import pyodbc
import pandas as pd 
import json
import os
#import api_general as ap
import requests 
def connect_db():
    try:
        PYODBC_Connection, df, sts = import_initialization()        
        cnxn = pyodbc.connect(PYODBC_Connection)                
        return cnxn, sts
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)                    
        return None, sts
def ret_pandas(sql):
    try:
        cnxn, sts = connect_db()   
        df = pd.read_sql(sql, cnxn)                          
        cnxn.commit()
        cnxn.close()        
        return df, "SUCCESS"
    except Exception as ex:                    
        return None, "FAILURE:  " + str(ex)        
def ret_json(sql):
    try:        
        data, sts = ret_pandas(sql)
        if (sts == "SUCCESS"):
            jsonstring = data.to_json(orient='index')
        else:
            sts = "FAILURE"
            jsonstring = None
        return jsonstring, sts          
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)        
        return None, sts   
def run_sql(sql):
    try:
        cnxn, sts = connect_db()
        cursor = cnxn.cursor()            
        cursor.execute(sql)
        cnxn.commit()
        cnxn.close()
        sts="SUCCESS"        
        return sts 
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)        
        return sts   

def import_initialization():    
    try:    
        df = pd.read_csv(r'InitializationFile.csv')        
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