import pyodbc
import pandas as pd
from constants import *

def read_excel_to_df(file_name, sheet_name):
    df = pd.read_excel(open(file_name, 'rb'), sheet_name=sheet_name, engine='openpyxl')
    df = df.reset_index(drop=True)
    return df

def get_items_from_db(conn_string):
    conn = pyodbc.connect(conn_string)
    str_query = QTY_BY_WAREHOUSE
    df = pd.read_sql(str_query, conn)
    return df