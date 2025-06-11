import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import random
import time
from chatbot import response_generator

load_dotenv()

global OPENAI_API_KEY


st.set_page_config(
    layout="wide",
    page_title="Football Data Analysis",
    page_icon="⚽",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <link rel="stylesheet" type="text/css" href="static/style.css">
""", unsafe_allow_html=True)


manual, chatbot, eda, scraper = st.tabs(["📖 Manual"
                                             , "🤖 Ask Chatbot!"
                                             , "📈 Do Your Own Data Analysis"
                                             , "📡 Web Scraper"])

with eda:

    st.markdown("### ⚽ Football Data Analysis Dashboard")
    col1, col2, col3, col4 = st.columns(4)

        
    engine = create_engine(os.getenv('FOOTBALL_URI'))
    conn = engine.connect()


    results = conn.execute(text("SELECT DISTINCT home_team_name from match ORDER BY home_team_name limit 5;"))
    team_list = [row[0] for row in results]

    with col1:
        season = st.selectbox(
            "Season",
            team_list,
            index=0
        )

    conn.close()



with manual:
    engine = create_engine(os.getenv('FOOTBALL_URI'))
    conn = engine.connect()
    
    tables_query = "SELECT table_name AS \"Tablo Adı\" FROM information_schema.tables \
                    WHERE table_schema='public' AND table_type='BASE TABLE';"
    
    df = pd.read_sql_query(tables_query, conn)

    st.subheader("Tüm Tabloların Bilgisi")
    st.dataframe(df)

    for table_name in df["Tablo Adı"]:
        
        tables_info_query = f"SELECT column_name AS \"Kolon Adı\", data_type AS \"Veri Tipi\", is_nullable AS \"Boş Tanımlanabilir\" \
                                FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table_name}'"
        
        sample_rows = f"SELECT * FROM {table_name} LIMIT 5;"
        
        df1 = pd.read_sql_query(tables_info_query, conn)

        st.subheader(f"{table_name} Tablosu İçeriği", divider="rainbow")
        st.dataframe(df1)

        df2 = pd.read_sql_query(sample_rows, conn)

        st.markdown("#### Örnek Veri")
        st.dataframe(df2)

    conn.close()



with chatbot:
    with st.popover("Enter your OpenAI API Key"):
        OPENAI_API_KEY = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Let's start chatting! 👇 \
                                  <br><br><b>💡 Try asking: </b><br><br> \
                                  - Show me the top 5 teams by goals scored <br>\
                                  - Compare possession stats between teams <br>\
                                  - What's the trend in expected goals?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    if user_input := st.chat_input("Ask me anything!"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input, unsafe_allow_html=True)

        with st.chat_message("assistant"):
            if not OPENAI_API_KEY:
                st.info("Please add your OpenAI API key to continue.")
                st.stop()
            message_placeholder = st.empty()
            full_response = ""
            assistant_response = response_generator(conn, user_input)
            # assistant_response_ = random.choice(
            #     [
            #         "Hello there! How can I assist you today?",
            #         "Hi, human! Is there anything I can help you with?",
            #         "Do you need help?",
            #     ]
            # )
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.rerun()

    conn.close()


with scraper:
    pass



