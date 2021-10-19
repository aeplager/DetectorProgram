import pandas as pd
import sqldata as sq
import pyodbc
import requests
try:    
    #cnxn, sts = sq.connect_db()
    sql = 'EXEC [WebSite].[FileMaxGetInfo]'
    df, sts = sq.ret_pandas(sql)
    print(df)
except Exception as ex:            
    sts = "FAILURE:  " + str(ex)   
    print(sts)