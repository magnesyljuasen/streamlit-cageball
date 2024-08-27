import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
import plotly.express as px

def show_scoreboard(df):
    fig = px.bar(
        df, 
        x=df.index, 
        y='Poeng', 
        color_discrete_sequence=['#1d3c34']
        )
    fig.update_layout(
        xaxis_tickangle=-45,
        margin=dict(l=50,r=50,b=10,t=10,pad=0),
        yaxis=dict(dtick=1, title="Poeng"),
        height=250
        )
    st.plotly_chart(fig, use_container_width=True, config = {'displayModeBar': False, 'staticPlot': True})


def get_scoreboard(df):
    df = df.set_index('-')
    df['Poeng'] = df.sum(axis=1)
    df = df['Poeng']
    df_sorted = df.sort_values(ascending=False)
    return df_sorted
    

def analyze_dfs(df1, df2):
    for index, row in df2.iterrows():
        for j in range(0, len(df1.columns)):
            date_column = row.index[j]
            winner = row[date_column]        
            if winner == 'Lag 1':
                df1[date_column] = df1[date_column].replace('Lag 1', 1)
                df1[date_column] = df1[date_column].replace('Lag 2', 0)
            elif winner == 'Lag 2':
                df1[date_column] = df1[date_column].replace('Lag 2', 1)
                df1[date_column] = df1[date_column].replace('Lag 1', 0)
    return df1

def find_cageball_date(df_participants):
    data = df_participants.columns[1:]
    date_series = pd.Series(pd.to_datetime(data))
    today = pd.to_datetime(datetime.now().date())
    if today in date_series.values:
        next_date = today
    else:
        next_date = date_series[date_series >= today].min()
    return today, next_date

@st.cache_resource(show_spinner=False)
def read_excel():
    df_participants = pd.read_excel('cageball_data.xlsx')[1:]
    df_winner = pd.read_excel('cageball_data.xlsx').head(1)
    return df_participants, df_winner

def embed_url(url, height=600):
    iframe_html = f"""
    <iframe src="{url}" width="100%" height="{height}px" style="border:none;"></iframe>
    """
    components.html(iframe_html, height=height)

#--
# Start app
#--

st.set_page_config(
    layout='wide', 
    initial_sidebar_state='expanded',
    page_title="Fantasy Cageball",
    )

with open("src/styles/main.css") as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

main_body_logo = "src/img/av-verktøy.png"
sidebar_logo = "src/img/av-logo-1.png"

st.logo(sidebar_logo, icon_image=main_body_logo)

df_participants, df_winner = read_excel()
df_results = analyze_dfs(df1=df_participants, df2=df_winner)
today, next_date = find_cageball_date(df_participants)
df_scoreboard = get_scoreboard(df_results)



with st.sidebar:
    st.title('Cageball med Asplan Viak')
    #st.image("src/img/asplanviak_1.jpg", use_column_width=True)
    selected_page = st.radio('Navigasjon', options=['Påmelding', 'Poengtavle'])

if selected_page == 'Påmelding':
    st.title('Påmelding')
    st.info('⚽ *Mot til å angripe, glød i skoene og respekt på banen!*')
    doodle_link = "https://doodle.com/meeting/organize/id/aMojxY1d"
    st.markdown(f'''<a target="parent" style="
                color: white; 
                background-color: #F6F8F1; 
                border: none; 
                transition-duration: 0.4s; 
                font-weight:600; 
                font-size: 20px; 
                border-radius: 15px; 
                text-align: center; 
                padding: 1rem; 
                min-height: 60px; 
                display: inline-block; 
                box-sizing: border-box; 
                width: 100%;
                " href="{doodle_link}">Meld deg på her!</a>''', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.image('src/img/asplanviak_1.jpg', use_column_width=True)
    with c2:
        st.image('src/img/asplanviak_2.jpg', use_column_width=True)


if selected_page == 'Poengtavle':
    st.title('Poengtavle')
    st.info('🏆 *Topp 3 - Antall seiere*')
    show_scoreboard(df_scoreboard.head(3))
    st.success(f'🏅 AV-M.V.P: **{df_scoreboard.head(1).index[0]}**')
    st.success(f'🐐 AV-G.O.A.T: ?')
    
if selected_page == 'Data':
    st.dataframe(df_participants, use_container_width=True, height=400)
    st.dataframe(df_winner, use_container_width=True)

#if selected_page == 'Hvem heier du på?':
#    cheering = st.selectbox('Hvem heier du på?', options=df_scoreboard.index.values, index=None, placeholder='Velg en fotballspiller...')
#    if cheering == 'Magne':
#        st.success('Riktig svar!')
#        st.balloons()
#    elif cheering == None:
#        pass
#    else:
#        st.warning('Velg en annen...')
















