import streamlit as st
from streamlit.logger import get_logger
from schema import db_connect

LOGGER = get_logger(__name__)


st.title('Challenge App')

stm = 'select * from challengers limit 10'
df = db_connect(stm)

st.dataframe(df)