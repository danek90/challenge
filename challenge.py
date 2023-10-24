import streamlit as st
from streamlit.logger import get_logger
from util import *
from dataclasses import dataclass, fields
import datetime
from typing import Any
import polars as pl

logger = get_logger(__name__)

# st.set_page_config(page_title="Challenger Stats", layout="wide", initial_sidebar_state="expanded")

@dataclass
class Challenger:
    '''class for challenger'''
    full_name: str
    first_name: str
    # last_name: str
    # gender: str
    # birth: datetime.date
    # death: datetime.date
    # hometown: str

def populate_chalengers():
    stm = '''select distinct c.* 
            from daily_history dh 
            inner join challengers c 
            on c.ch_id = dh.ch_id '''
    challengers_df = db_connect(stm)
    challenger_ids = dict(zip(challengers_df.ch_name, challengers_df.ch_id))
    challenger_ids["Select Challenger"]= 0
    return challengers_df, challenger_ids

def challenger_stats(challengers, ch_id):
    ch_df = challengers.loc[challengers['ch_id'] == ch_id]
    ch_df.drop(['ch_id', 'legal_name'], axis=1, inplace=True)
    ch_df_T = ch_df.T.astype(str)
    ch_df_T.rename(columns={ch_df_T.columns[0]:'Challenger Info'}, inplace=True)
    return ch_df_T

def challenger_record(ch_id):
    stm=f'''
        select c.ch_id 
        , count(distinct dh.daily_id) as dailies_played
        , count(distinct dh.daily_id) FILTER (WHERE dh.daily_team_result = 'win') AS dailies_won
        , count(distinct eh.elim_id) as elims_played
        , count(distinct eh.elim_id) FILTER (WHERE eh.elim_result = 'win') AS elims_won
        from challengers c 
        inner join daily_history dh on c.ch_id = dh.ch_id 
        inner join elim_history eh on eh.ch_id = c.ch_id  
        where c.ch_id = {ch_id}
        group by c.ch_id
        '''
    ch_record_df = db_connect(stm)
    ch_record_df.drop(['ch_id'], axis=1, inplace=True)
    ch_record_df_T = ch_record_df.T.astype(str)
    ch_record_df_T.rename(columns={ch_record_df_T.columns[0]:'Challenger Stats'}, inplace=True)
    return ch_record_df_T

challengers_df, challenger_ids = populate_chalengers()

ch_select = st.selectbox('Select Challenger', list(challenger_ids.keys()), index=list(challenger_ids.keys()).index('Select Challenger'))

if ch_select == 'Select Challenger':
    st.write("Welcome to the Challenger App. Please select a Challenger.")
else:
    ch_id = challenger_ids[ch_select]

    col1, col2 = st.columns(2)

    challenger_df = challenger_stats(challengers_df, ch_id)
    col1.dataframe(data=challenger_df)

    ch_record_df = challenger_record(ch_id)
    col1.dataframe(data=ch_record_df)

    img = pull_image(ch_id=ch_id)
    col2.image(img)
