import streamlit as st
from streamlit.logger import get_logger
from util import *
from dataclasses import dataclass, fields
import datetime
from typing import Any
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.set_page_config(page_title="Challenger Summary")

def win_percentage():

    stm='''with elim_wins as (
select 
eh.ch_id 
, c.ch_name
, c.gender
, EXTRACT('YEAR' FROM AGE(CURRENT_DATE, c.birth)) AS ch_age
, count(elim_id) as elim_count
, count(distinct eh.elim_id) FILTER (WHERE eh.elim_result = 'win') AS elims_won
from elim_history eh 
inner join challengers c on eh.ch_id =c.ch_id 
group by eh.ch_id, c.ch_name, c.ch_name, c.gender, c.birth 
)
SELECT
    ch_name
    , elims_won
    , elim_count
    , ch_name
    , gender
    , ch_age
    , RANK() OVER (ORDER BY (elims_won * 100.0 / elim_count) DESC) AS win_percentage_rank
FROM elim_wins;
'''
    ch_percent_df = db_connect(stm)
    return ch_percent_df


st.write("Summerized Values")


ch_percent_df = win_percentage()
fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(10, 10))
plt.subplots_adjust(hspace=0.5)

ax[0].hist(ch_percent_df['elims_won'][ch_percent_df['gender'] == "male"]
           , bins=10, alpha=0.5, color='blue')
ax[0].set_xlabel('Male Eliminations Won')
ax[0].set_ylabel('Frequency')
ax[0].set_title('Histogram of Male Challenger Wins')
ax[0].set_xlim(0, 16)
ax[0].set_xticks(np.arange(0, 16, 1))


ax[1].hist(ch_percent_df['elims_won'][ch_percent_df['gender'] == "female"]
           , bins=10, alpha=0.5, color='blue')
ax[1].set_xlabel('Female Eliminations Won')
ax[1].set_ylabel('Frequency')
ax[1].set_title('Histogram of Female Challenger Wins')
ax[1].set_xlim(0, 16)
ax[1].set_xticks(np.arange(0, 16, 1))

ax[2].set_title('Elimination Wins by Gender')
ax[2].set_xlabel('Gender')
ax[2].set_ylabel('Wins')
ax[2].boxplot([ch_percent_df[ch_percent_df['gender'] == 'female']['elims_won'], ch_percent_df[ch_percent_df['gender'] == 'male']['elims_won']],
            labels=['Female', 'Male'])

st.pyplot(fig)

stats_by_gender = ch_percent_df.groupby('gender')['elims_won'].agg(['mean', 'median', 'min', 'max', 'std'])
Q1 = ch_percent_df.groupby('gender')['elims_won'].quantile(0.25)
Q3 = ch_percent_df.groupby('gender')['elims_won'].quantile(0.75)
IQR = Q3 - Q1
stats_by_gender['IQR'] = IQR

# Rename columns for clarity
stats_by_gender.columns = ['Mean', 'Median', 'Min', 'Max', 'Standard Deviation', 'IQR']

# Display the summary table
st.write(stats_by_gender)



# st.title("Player Performance Scatter Plot")

# x_axis = st.selectbox("Select X-axis Data", ch_percent_df.columns, index=list(ch_percent_df.keys()).index('elim_count'))
# y_axis = st.selectbox("Select Y-axis Data", ch_percent_df.columns, index=list(ch_percent_df.keys()).index('elims_won'))
# fig, ax = plt.subplots()
# ax.scatter(ch_percent_df[x_axis], ch_percent_df[y_axis])
# ax.set_xlabel(x_axis)
# ax.set_ylabel(y_axis)
# st.pyplot(fig)

