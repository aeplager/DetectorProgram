import pyodbc
import pandas as pd 
import json
import os
#import api_general as ap
import requests 
import sqlalchemy
from sqlalchemy import create_engine, event
import platform
path = "C:\\BlenderFiles\\"
os.chdir(path)
cwd = os.getcwd() 
print("Current Directory:", cwd)
 
# Get the directory of
# script
path = os.path.realpath(__file__)
separator = "\\"
source_file_name = "InitializationFileWindows.csv"
if not ("windows" in platform.system().lower()):
    separator = "/"
    source_file_name = "InitializationFileUbuntu.csv"
iloc = len(path)
iloc = path.rfind(separator,0, iloc)
path = path[:iloc] + separator + source_file_name
print("Script path:", path)
# if not ("windows" in platform.system().lower()):
#     path = "/home/amagcons/Documents/BlenderFiles/PCScripts/InitializationFile.csv" 
# else:
#     path = "/home/amagcons/Documents/BlenderFiles/PCScripts/InitializationFile.csv" 