import psycopg2
import os
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

DATABASE = os.getenv("PGDATABASE")
HOST = os.getenv("PGHOST")
PASSWORD = os.getenv("PGPASSWORD")
PORT = os.getenv("PGPORT")
USER = os.getenv("PGUSER")


def db_connect(stm):
    with psycopg2.connect(database = DATABASE, user = USER, 
                        host= HOST, password = PASSWORD, port = PORT) as conn:
        data = pd.read_sql_query(stm, conn)
    return data

def pull_image(ch_id):
    c = f'https://thechallenge.fandom.com/?curid={ch_id}'
    reqs = requests.get(c)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    img = soup.find("a", {"class":"image image-thumbnail"}, href=True)['href']
    img = re.sub(r'/revision.*$',"", img)
    return img