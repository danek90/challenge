import psycopg2
import os
import pandas as pd

DATABASE = os.getenv("PGDATABASE")
HOST = os.getenv("PGHOST")
PASSWORD = os.getenv("PGPASSWORD")
PORT = os.getenv("PGPORT")
USER = os.getenv("PGUSER")

def db_connect(stm):
    with psycopg2.connect(database = DATABASE, 
                            user = USER, 
                            host= HOST,
                            password = PASSWORD,
                            port = PORT) as conn:
        # stm = "SELECT * FROM challengers;"
        data = pd.read_sql_query(stm, conn)

    
    return data
