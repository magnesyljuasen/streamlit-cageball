import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime

def find_cageball_date(df_participants):
    data = df_participants.columns[1:]

    # Create a Pandas Series
    date_series = pd.Series(pd.to_datetime(data))

    # Get today's date
    today = pd.to_datetime(datetime.now().date())

    # Check if today's date is in the series
    if today in date_series.values:
        next_date = today
    else:
        # Find the next date if today's date is not in the series
        next_date = date_series[date_series >= today].min()

    return today, next_date


@st.cache_resource(show_spinner=False)
def read_excel():
    df_participants = pd.read_excel('cageball_data.xlsx')[1:]
    df_winner = pd.read_excel('cageball_data.xlsx').head(1)
    return df_participants, df_winner

def embed_url(url, height=600):
    #height_string = f"{height}px"
    iframe_html = f"""
    <iframe src="{url}" width="100%" height="{height}px" style="border:none;"></iframe>
    """
    components.html(iframe_html, height=height)

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open("src/styles/main.css") as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

main_body_logo = "src/img/av-verktøy.png"
sidebar_logo = "src/img/av-logo-1.png"

st.logo(sidebar_logo, icon_image=main_body_logo)


st.title('Fantasy Cageball - Asplan Viak FC ')
todays_date = datetime.now().strftime("%Y-%m-%d")

doodle_link = "https://doodle.com/meeting/organize/id/aMojxY1d"
st.markdown(f"[⚽ Trykk her for påmelding (doodle)]({doodle_link})")

df_participants, df_winner = read_excel()
today, next_date = find_cageball_date(df_participants)

st.header('Historikk')
st.dataframe(df_participants, use_container_width=True, height=150)
st.dataframe(df_winner, use_container_width=True)

st.header('')

st.image("src/img/asplanviak_1.jpg", use_column_width=True)











