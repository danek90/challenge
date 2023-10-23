import streamlit as st
from streamlit.logger import get_logger
from util import *

LOGGER = get_logger(__name__)


st.set_page_config(page_title="Challenger Stats", layout="wide", initial_sidebar_state="expanded")

stm = 'select * from challengers'
challengers = db_connect(stm)

challenger_names = list(challengers[['ch_id','ch_name']].apply(tuple, axis=1))

ch_select = st.selectbox('Select Challenger', challengers['ch_name'])

ch_wiki = [x for x, y in challenger_names if y == ch_select][0]

col1, col2 = st.columns(2)
img = pull_image(ch_id=ch_wiki)

col2.image(img, caption=ch_select)

stm = f'select * from challengers where ch_id = {ch_wiki}'
ch_stats = db_connect(stm).to_dict('records')

s_first_name = ch_stats[0]['first_name']
s_last_name = ch_stats[0]['last_name']
s_gender = ch_stats[0]['gender']
birth_date = ch_stats[0]['birth']
death_date = ch_stats[0]['death']
hometown = ch_stats[0]['hometown']

col1.write(f'''
First Name: {s_first_name} \n
Last Name: {s_last_name} \n
Gender: {s_gender} \n
Birth Date: {birth_date} \n
Death Date: {death_date} \n
Home Town: {hometown} \n
''')