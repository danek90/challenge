import streamlit as st
from streamlit.logger import get_logger
from util import *
from dataclasses import dataclass, fields
import datetime
from typing import Any
import matplotlib.pyplot as plt

logger = get_logger(__name__)

st.set_page_config(page_title="Challenger Stats", layout="wide")


def populate_chalengers():
    stm = '''select distinct c.* from challengers c inner join daily_history dh on c.ch_id = dh.ch_id order by ch_name'''
    challengers_df = db_connect(stm)
    challenger_ids = dict(zip(challengers_df.ch_name, challengers_df.ch_id))
    challenger_ids["Select Challenger"]= 0
    return challengers_df, challenger_ids

def challenger_info(challengers, ch_id):
    ch_df = challengers.loc[challengers['ch_id'] == ch_id]
    ch_df.drop(['ch_id', 'legal_name'], axis=1, inplace=True)
    ch_df_T = ch_df.T.astype(str)
    ch_df_T.rename(columns={ch_df_T.columns[0]:'Challenger Info'}, inplace=True)
    return ch_df_T

def challenger_stats(ch_id):

    stm=f'''select c.ch_id 
        , count(distinct d.season_id) as seasons_played
        , count(distinct dh.daily_id) as dailies_played
        , count(distinct dh.daily_id) FILTER (WHERE dh.daily_team_result = 'win') AS dailies_won
        , count(distinct eh.elim_id) as elims_played
        , count(distinct eh.elim_id) FILTER (WHERE eh.elim_result = 'win') AS elims_won
        , count(distinct fh.final_id) as finals_played
        , count(distinct fh.final_id) FILTER (WHERE fh.final_result  = 'first') AS finals_won
        from challengers c 
        inner join daily_history dh on c.ch_id = dh.ch_id 
        inner join dailies d on dh.daily_id = d.daily_id
        inner join elim_history eh on eh.ch_id = c.ch_id  
        left join final_history fh on c.ch_id = fh.ch_id  
        where c.ch_id = {ch_id}
        group by c.ch_id'''
    ch_stats_df = db_connect(stm)
    ch_stats_df.drop(['ch_id'], axis=1, inplace=True)
    ch_stats_df_T = ch_stats_df.T.astype(str)
    ch_stats_df_T.rename(columns={ch_stats_df_T.columns[0]:'Challenger Stats'}, inplace=True)
    return ch_stats_df, ch_stats_df_T

def elim_table(ch_id):
    stm=f'''
    select distinct eh.elim_id
, (select e.season_id from eliminations e where e.elim_id = eh.elim_id) as season
, (select e.elim_in_season from eliminations e where e.elim_id = eh.elim_id) as elim_in_season
, (select e.elim_name from eliminations e where e.elim_id = eh.elim_id) as elim_name
, eh.ch_id
, c.ch_name
, (select c.ch_name from challengers c where c.ch_id = eh.elim_partner_id) as partner
, (select c.ch_name from challengers c where c.ch_id = eh.opponent_id) as opponent_1
, (select c.ch_name from challengers c where c.ch_id = eh.opponent_partner_id) as oppondent_2
, eh.elim_result 
, (select em.method_class from elim_method em where em.method_id = eh.method_id) as reason_for_elim 
from elim_history eh
inner join challengers c on eh.ch_id = c.ch_id
where eh.ch_id = {ch_id}
order by elim_id'''
    ch_elim_df = db_connect(stm)
    ch_elim_df.drop(['ch_id', 'elim_id'], axis=1, inplace=True)
    return ch_elim_df

def durration_in_season(ch_id):
    stm=f'''
    select dh.ch_id 
    , d.season_id 
    , count(dh.daily_id) as dailies_played
    , (select max(d2.daily_in_season)
            from dailies d2
            where d2.season_id = d.season_id 
            group by d2.season_id) as max_dailies
    , exists(select 1 
            from final_history fh 
            left join finals f on fh.final_id = f.final_id 
            where fh.ch_id = dh.ch_id
            and f.season_id = d.season_id) as made_final
    from daily_history dh
    right join dailies d on d.daily_id  = dh.daily_id 
    where ch_id = {ch_id}
    group by dh.ch_id, d.season_id 
    order by season_id
    '''
    ch_duration_df = db_connect(stm)
    ch_duration_df['max_dailies'] = ch_duration_df.apply(lambda row: row['dailies_played'] if row['made_final'] == True
                                                         and row['dailies_played'] != row['max_dailies'] 
                                                         else row['max_dailies'], axis=1)
    ch_duration_df['max_dailies_w_final'] = ch_duration_df.apply(lambda row: row.max_dailies + 1 if row['made_final'] == False
                                                                 else row.max_dailies, axis=1)
    ch_duration_df['percent_complete'] = round(100 * (ch_duration_df.dailies_played / ch_duration_df.max_dailies_w_final), 2)
    avg_duration = round(ch_duration_df['percent_complete'].mean(), 2)

    ch_duration_df = ch_duration_df[['season_id', 'percent_complete']]
    return avg_duration, ch_duration_df


challengers_df, challenger_ids = populate_chalengers()

ch_select = st.selectbox('Select Challenger', list(challenger_ids.keys()), index=list(challenger_ids.keys()).index('Select Challenger'))

if ch_select == 'Select Challenger':
    st.write("Welcome to the Challenger App. Please select a Challenger.")
else:
    ch_id = challenger_ids[ch_select]

    col1, col2 = st.columns(2)
    img = pull_image(ch_id=ch_id)
    col2.image(img)

    challenger_df = challenger_info(challengers_df, ch_id)
    col1.dataframe(data=challenger_df)

    ch_stats_df, ch_stats_df_T = challenger_stats(ch_id)
    col1.dataframe(data=ch_stats_df_T)

    avg_duration, ch_duration_df = durration_in_season(ch_id)
    st.write(f"Average length in Season: {str(avg_duration)}%")
    st.dataframe(ch_duration_df,hide_index=True)

# ['(%) Dailies Won', '(%) Eliminations Won', '(%) Length In Season', 'Number of Seasons']

    dailies_won_p = ch_stats_df.dailies_won / ch_stats_df.dailies_played
    elim_won_p = ch_stats_df.elims_won / ch_stats_df.elims_played
    seaons_played = ch_stats_df.seasons_played[0]

    player_data = [round((dailies_won_p[0]*100),2)
                       , round((elim_won_p[0]*100),2)
                       , avg_duration]
    
    categories = ['Dailies Won', 'Eliminations Won', 'Length In Season']
    num_vars = len(categories)

    # Calculate angles for each variable
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    angles += angles[:1]  # Close the plot
    player_data += player_data[:1]

    # Create a radar plot
    fig, ax = plt.subplots(subplot_kw=dict(polar=True), figsize=(6, 6))

    ax.plot(angles, player_data, color='#1aaf6c', linewidth=1)
    ax.fill(angles,player_data, color='#1aaf6c', alpha=0.25)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), categories)
    for label, angle in zip(ax.get_xticklabels(), angles):
        if angle in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')
    ax.set_ylim(0, 100)
    ax.set_rlabel_position(180 / num_vars)
    # ax.set_xticks(angles[:-1])
    # ax.set_xticklabels(categories)
    # ax.set_yticklabels([])  # Hide y-axis labels

    ax.tick_params(colors='#222222')
    ax.tick_params(axis='y', labelsize=8)
    ax.grid(color='#AAAAAA')
    ax.spines['polar'].set_color('#222222')
    ax.set_facecolor('#FAFAFA')
    ax.set_title('Challenger Stats', y=1.08)

    # ax.set_yticks(0,100, 10)
    # Display the radar plot in the Streamlit app
    col2.pyplot(fig)

    ch_elim_df = elim_table(ch_id)
    st.dataframe(data=ch_elim_df,hide_index=True)


